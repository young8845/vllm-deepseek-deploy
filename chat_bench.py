import time
from openai import OpenAI

VLLM_URL = "http://localhost:30004"
MODEL = "DeepSeek-V4-Flash"

client = OpenAI(base_url=f"{VLLM_URL}/v1", api_key="unused")

start = time.time()
resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What is PagedAttention in one sentence?"}],
    max_tokens=80,
    temperature=0.7,
    top_p=0.8,
    extra_body={"top_k": 20, "chat_template_kwargs": {"enable_thinking": False}},
)
elapsed = time.time() - start

print(f"Response ({elapsed:.2f}s, {resp.usage.completion_tokens} tokens):")
print(resp.choices[0].message.content)

print(f"\nUsage: {resp.usage.prompt_tokens} prompt + {resp.usage.completion_tokens} completion = {resp.usage.total_tokens} total")
