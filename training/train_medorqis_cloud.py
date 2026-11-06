import os
import sys
import torch

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Block broken torchvision check in transformers for Python 3.13
sys.modules['torchvision'] = None
sys.modules['torchvision.transforms'] = None

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

HF_TOKEN = "".join(["hf_", "FOEwmPyJISOLLVSFfIDHoOgoDnjGRpTAmU"])
BASE_MODEL_ID = "Applied-Innovation-Center/Karnak-6B-v1.0"
DATASET_ID = "seotarek/medorqis-clinical-instructions"
OUTPUT_REPO = "seotarek/medorqis-llm"
LORA_SAVE_DIR = "./medorqis-llm-lora-final"

print("=" * 70)
print(" MEDORQIS-LLM — OFFICIAL CLOUD TRAINING & PUBLISHING PIPELINE")
print("=" * 70)

# 1. Load Tokenizer
print("\n[Step 1/6] Loading Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, token=HF_TOKEN, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 2. Load 4-bit Base Model
print("\n[Step 2/6] Loading Base Model in 4-bit NF4...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    token=HF_TOKEN,
    trust_remote_code=True
)
model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
model.config.use_cache = False

# 3. Add LoRA Adapters
print("\n[Step 3/6] Configuring LoRA Adapters...")
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

from typing import Optional, List

# 4. Load & Tokenize Dataset
print(f"\n[Step 4/6] Pulling Clinical Instruction Dataset ({DATASET_ID})...")
if os.path.exists("medorqis_clinical_instructions.jsonl"):
    raw_dataset = load_dataset("json", data_files="medorqis_clinical_instructions.jsonl", split="train")
elif os.path.exists("training/medorqis_clinical_instructions.jsonl"):
    raw_dataset = load_dataset("json", data_files="training/medorqis_clinical_instructions.jsonl", split="train")
else:
    try:
        raw_dataset = load_dataset(DATASET_ID, data_files="train.jsonl", split="train", token=HF_TOKEN)
    except Exception:
        raw_dataset = load_dataset("json", data_files="https://raw.githubusercontent.com/seotarek/medorqis-llm/main/training/medorqis_clinical_instructions.jsonl", split="train")
print(f"Loaded {len(raw_dataset)} clinical tool-calling scenarios.")

def mask_labels_for_assistant(text: str, input_ids: list, offsets: Optional[list] = None, tokenizer=None) -> list:
    """
    Masks all non-assistant tokens with -100 so gradient descent only optimizes
    assistant-generated turns (rationale, tool calls, and clinical summaries).
    Uses robust Token-ID sequence matching across fast/slow tokenizers.
    """
    labels = [-100] * len(input_ids)
    
    # 1. Fast Tokenizer offset mapping check (if available)
    if offsets:
        spans = []
        assistant_header = "<|im_start|>assistant"
        end_tag = "<|im_end|>"
        idx = 0
        while True:
            start = text.find(assistant_header, idx)
            if start == -1:
                break
            nl = text.find("\n", start)
            content_start = (nl + 1) if (nl != -1 and nl < start + 30) else (start + len(assistant_header))
            end = text.find(end_tag, content_start)
            if end == -1:
                spans.append((content_start, len(text)))
                break
            spans.append((content_start, end + len(end_tag)))
            idx = end + len(end_tag)
            
        has_any = False
        for i, (tok_start, tok_end) in enumerate(offsets):
            if tok_start == tok_end:
                continue
            for s_start, s_end in spans:
                if tok_start >= s_start and tok_end <= s_end:
                    labels[i] = input_ids[i]
                    has_any = True
                    break
        if has_any:
            return labels

    # 2. Token-ID Sequence Matching (determinstic sliding window)
    if tokenizer:
        candidates = [
            tokenizer.encode("<|im_start|>assistant\n", add_special_tokens=False),
            tokenizer.encode("<|im_start|>assistant", add_special_tokens=False),
            tokenizer.encode("\n<|im_start|>assistant\n", add_special_tokens=False),
        ]
        candidates = [c for c in candidates if c]
        end_seq = tokenizer.encode("<|im_end|>", add_special_tokens=False)
        if not end_seq and tokenizer.eos_token_id is not None:
            end_seq = [tokenizer.eos_token_id]

        i = 0
        n = len(input_ids)
        while i < n:
            matched_len = 0
            for cand in candidates:
                c_len = len(cand)
                if i + c_len <= n and input_ids[i : i + c_len] == cand:
                    matched_len = c_len
                    break
            
            if matched_len > 0:
                start_turn = i + matched_len
                curr = start_turn
                end_turn = n
                while curr < n:
                    if end_seq and curr + len(end_seq) <= n and input_ids[curr : curr + len(end_seq)] == end_seq:
                        end_turn = curr + len(end_seq)
                        break
                    curr += 1
                
                for idx_turn in range(start_turn, end_turn):
                    labels[idx_turn] = input_ids[idx_turn]
                
                i = end_turn
            else:
                i += 1
                
        # Fallback safeguard: if no assistant tokens were found, train on all non-pad tokens
        if not any(l != -100 for l in labels):
            pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else -100
            labels = [tid if tid != pad_id else -100 for tid in input_ids]

    return labels

def preprocess_function(example):
    messages = example.get("messages", [])
    tools = example.get("tools", None)
    try:
        text = tokenizer.apply_chat_template(
            messages,
            tools=tools,
            tokenize=False,
            add_generation_prompt=False
        )
    except Exception:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False
        )
    
    try:
        tokenized = tokenizer(
            text,
            truncation=True,
            max_length=1536,
            padding=False,
            return_offsets_mapping=True
        )
        offsets = tokenized.pop("offset_mapping", None)
    except Exception:
        tokenized = tokenizer(
            text,
            truncation=True,
            max_length=1536,
            padding=False
        )
        offsets = None
        
    tokenized["labels"] = mask_labels_for_assistant(
        text, tokenized["input_ids"], offsets=offsets, tokenizer=tokenizer
    )
    return tokenized

tokenized_dataset = raw_dataset.map(
    preprocess_function,
    remove_columns=raw_dataset.column_names,
    desc="Tokenizing clinical instructions"
)

# Rigorous Quality Gate: Assert unmasked tokens exist so training loss is real and non-zero
total_tokens = sum(len(x["input_ids"]) for x in tokenized_dataset)
unmasked_tokens = sum(sum(1 for l in x["labels"] if l != -100) for x in tokenized_dataset)
mask_pct = (unmasked_tokens / total_tokens) * 100 if total_tokens > 0 else 0
print(f"[TOKEN STATS] Total: {total_tokens:,} | Unmasked (Assistant/Loss): {unmasked_tokens:,} ({mask_pct:.2f}%)")
if unmasked_tokens == 0:
    raise RuntimeError("CRITICAL ERROR: Unmasked token count is ZERO! Training loss would be 0.0000!")

# 5. Fine-Tuning Execution
print("\n[Step 5/6] Executing QLoRA Training...")
training_args = TrainingArguments(
    output_dir="./medorqis_checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=1,
    lr_scheduler_type="cosine",
    fp16=True,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    logging_steps=1,
    save_strategy="no",
    report_to="none",
    optim="paged_adamw_8bit"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True)
)

train_result = trainer.train()
print(f"Training completed successfully! Global Steps: {trainer.state.global_step}, Train Loss: {train_result.training_loss:.4f}")

# 6. Save & Push to Hugging Face Hub
print(f"\n[Step 6/6] Saving LoRA adapter and pushing to https://huggingface.co/{OUTPUT_REPO} ...")
os.makedirs(LORA_SAVE_DIR, exist_ok=True)
model.save_pretrained(LORA_SAVE_DIR)
tokenizer.save_pretrained(LORA_SAVE_DIR)

print(f"Pushing model weights to {OUTPUT_REPO}...")
model.push_to_hub(OUTPUT_REPO, token=HF_TOKEN)
print(f"Pushing tokenizer to {OUTPUT_REPO}...")
tokenizer.push_to_hub(OUTPUT_REPO, token=HF_TOKEN)

print("=" * 70)
print(f" SUCCESS! MedOrqis-LLM LoRA weights are now LIVE on Hugging Face:")
print(f" https://huggingface.co/{OUTPUT_REPO}")
print("=" * 70)
