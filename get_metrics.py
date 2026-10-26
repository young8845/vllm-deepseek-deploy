import requests
import json

# 补充截图外未定义的变量
VLLM_URL = "http://localhost:30004"

def get_vllm_metrics(base_url=VLLM_URL):
    """Scrape vLLM Prometheus /metrics and return {name: value}."""
    r = requests.get(f"{base_url}/metrics")
    metrics = {}
    for line in r.text.split("\n"):
        # 跳过注释行（以#开头）和空行
        if line.startswith("#") or not line.strip():
            continue
        
        # 提取指标名称：比如 "vllm:num_requests_running{model_name='...'} 5.0"
        # split("{")[0] 拿到 vllm:num_requests_running
        # split()[0] 是双重保险，防止有的行没有花括号
        name = line.split("{")[0].split()[0]
        
        try:
            # 提取指标的值：取每行空格分割后的最后一个元素，转为浮点数
            metrics[name] = float(line.split()[-1])
        except (ValueError, IndexError):
            # 如果解析失败（比如格式不对），跳过这一行
            continue
    return metrics
# 获取所有指标
metrics = get_vllm_metrics()

print("Current vLLM Metrics:")
# 我们只挑几个我们最关心的核心指标来打印
for key in ["vllm:num_requests_running", "vllm:num_requests_waiting",
            "vllm:gpu_cache_usage_perc", "vllm:cpu_cache_usage_perc",
            "vllm:prompt_tokens_total", "vllm:generation_tokens_total"]:
    if key in metrics:
        # {key.replace('vllm:', '')} 把前缀去掉，显示得更清爽
        # {metrics[key]:g} 的 :g 意思是自动去掉小数点后多余的 0，比如 5.0 会显示为 5
        print(f"  {key.replace('vllm:', '')}: {metrics[key]:g}")

# 把所有抓取到的指标保存成 JSON 文件，方便后续分析
with open("outputs/metrics_snapshot.json", "w") as f:
    json.dump(metrics, f, indent=2)
print(f"\nFull metrics saved to outputs/metrics_snapshot.json")
