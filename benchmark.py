import time
import concurrent.futures
from openai import OpenAI
import requests

# ================= 补充的基础配置 =================
VLLM_URL = "http://localhost:30004"
MODEL = "DeepSeek-V4-Flash"
client = OpenAI(base_url=f"{VLLM_URL}/v1", api_key="unused")

# 引入之前写的获取 metrics 的函数
def get_vllm_metrics(base_url=VLLM_URL):
    r = requests.get(f"{base_url}/metrics")
    metrics = {}
    for line in r.text.split("\n"):
        if line.startswith("#") or not line.strip():
            continue
        name = line.split("{")[0].split()[0]
        try:
            metrics[name] = float(line.split()[-1])
        except (ValueError, IndexError):
            continue
    return metrics

# ================= 截图中的核心代码 =================
prompts = [
    "What is quantization?",
    "Explain KV caching briefly.",
    "What is continuous batching?",
    "Why is LLM inference memory-bound?",
    "What is PagedAttention?",
]

def _ask(prompt):
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60, temperature=0.7,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )

before = get_vllm_metrics()
print(f"Sending {len(prompts)} concurrent requests...\n")
start = time.time()

with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(prompts)) as pool:
    
    # 异步提交所有请求
    futures = {pool.submit(_ask, p): p for p in prompts}
    
    # 等待 0.5 秒，让请求在后台飞一会儿，然后去抓取 vLLM 的实时状态
    time.sleep(0.5)
    during = get_vllm_metrics()
    running = during.get("vllm:num_requests_running", "--")
    waiting = during.get("vllm:num_requests_waiting", "--")
    print(f"  [mid-flight]  running: {running}  |  waiting: {waiting}")

    # 按请求完成的先后顺序处理结果
    for f in concurrent.futures.as_completed(futures):
        resp = f.result()
        # 修复了截图中被截断的打印语句
        print(f"  done: '{futures[f][:40]}...' -> {resp.usage.completion_tokens} tokens")

elapsed = time.time() - start
after = get_vllm_metrics()
# 计算这期间总共生成了多少 token
tokens = after.get("vllm:generation_tokens_total", 0) - before.get("vllm:generation_tokens_total", 0)

print(f"\nAll {len(prompts)} completed in {elapsed:.2f}s")
if tokens > 0:
    print(f"Tokens generated: {tokens:g} | ~{tokens / elapsed:.1f} tokens/s")
