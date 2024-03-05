import torch
from transformers import pipeline, BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from haystack.nodes import PromptNode

model_name = "HuggingFaceH4/zephyr-7b-alpha"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    quantization_config=quantization_config,
    device_map="cuda"
)

def get_prompt_node(*args, **kwargs):
    return PromptNode(
        model_name_or_path="zephyr-7b-alpha",
        model_kwargs={"model":model, "tokenizer": tokenizer, 'device':None, 'stream': True},
        **kwargs
    )
    # 'task_name':'text2text-generation'

if __name__=="__main__":
    pn = get_prompt_node()
    pn("Can you help me with my homework?")