import math
from openai import OpenAI

VLLM_URL = "http://localhost:30004"
MODEL = "DeepSeek-V4-Flash"
client = OpenAI(base_url=f"{VLLM_URL}/v1", api_key="unused")

resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "The capital of France is"}],
    max_tokens=15,
    temperature=0.0,
    logprobs=True,
    top_logprobs=5,
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)

print(f"Response: {resp.choices[0].message.content.strip()}\n")
print("Token-by-token probabilities:\n")

for tok in resp.choices[0].logprobs.content[:8]:
    print(f"  Chosen: '{tok.token}' (logprob {tok.logprob:.2f})")
    
    if tok.top_logprobs:
        for alt in tok.top_logprobs[:5]:
            pct = math.exp(alt.logprob) * 100
            bar = "\u2588" * min(20, max(1, int(pct / 5)))
            print(f"      {pct:5.1f}% {bar} '{alt.token}'")
            
    print()
