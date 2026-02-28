from transformers import pipeline
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

Messages = list[dict[Literal["role", "content"], str]]

def completion_text(messages: Messages) -> tuple[str, Messages]:
    output = pipe(messages, max_new_tokens=10000) # type: ignore
    return output[-1]['generated_text'][-1]['content'], output[-1]['generated_text']