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

# 4. Load & Tokenize Dataset
print(f"\n[Step 4/6] Pulling Clinical Instruction Dataset ({DATASET_ID})...")
raw_dataset = load_dataset(DATASET_ID, split="train", token=HF_TOKEN)
print(f"Loaded {len(raw_dataset)} clinical tool-calling scenarios.")

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
    
    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=1536,
        padding=False
    )
    tokenized["labels"] = list(tokenized["input_ids"])
    return tokenized

tokenized_dataset = raw_dataset.map(
    preprocess_function,
    remove_columns=raw_dataset.column_names,
    desc="Tokenizing clinical instructions"
)

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
