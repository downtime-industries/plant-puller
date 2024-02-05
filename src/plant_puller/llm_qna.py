import torch
from transformers import pipeline, BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "HuggingFaceH4/zephyr-7b-alpha"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

print(torch.backends.mps.is_available())

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    quantization_config=quantization_config,
    device_map="cuda",
).eval()
generation_config = {
    "max_new_tokens": 256,
    "do_sample": True,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.95,
}

messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot.",
    },
    {"role": "user", "content": "Write me a sonnet that describes the everyday challenges of a developer advocate who is struggling with describing the intricacies of search relevance engineering."},
]

with torch.no_grad():
    inputs = tokenizer(
        tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True),
        return_tensors='pt',
    ).to(model.device)

    # .to(model.device)
    outputs = model.generate(
        **inputs,
        **generation_config,
        use_cache=True,
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))