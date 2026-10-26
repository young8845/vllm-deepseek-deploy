import time, requests

# 替换为你实际的端口，比如 30004
VLLM_URL = "http://localhost:30004" 

print("Waiting for vLLM server...")
for attempt in range(60):
    try:
        r = requests.get(f"{VLLM_URL}/v1/models", timeout=5)
        if r.status_code == 200:
            MODEL = r.json()["data"][0]["id"]
            break
    except requests.ConnectionError:
        pass
    time.sleep(5)
    if attempt % 6 == 5:
        print(f"  Still waiting... {(attempt + 1) * 5}s elapsed")
else:
    raise RuntimeError("vLLM server not reachable after 5 minutes.")

print(f"Connected to {VLLM_URL} - model: {MODEL}")
