# vllm-deepseek-deploy
# vLLM DeepSeek-V4 部署与测试脚本

本项目记录了在国产GPU 环境下，使用 vLLM 部署 DeepSeek-V4-Flash 大模型的过程，并包含连通性测试、性能指标监控和底层概率解析脚本。

## 🛠️ 环境依赖
- 硬件：沐曦 C500 GPU (8卡)
- 推理框架：vLLM (基于 MacaRT 适配版)
- 运行环境：Docker / Python 3.10+

## 📂 文件说明
- `docker-compose.yml`：一键启动模型的配置文件（含沐曦 GPU 设备挂载与环境变量）。
- `check_server.py`：服务就绪探针，验证 API 是否连通。
- `chat_bench.py`：对话测试脚本，统计首字延迟（TTFT）与生成速率（Tokens/s）。
- `logprob_test.py`：打印模型生成每个 Token 时的 Top-5 概率分布，用于分析模型行为。
- `get_metrics.py`：抓取 vLLM 底层的 Prometheus 监控指标。

## 🚀 快速开始
1. 修改 `docker-compose.yml` 中的模型路径和镜像名。
2. 启动服务：
   ```bash
   docker compose up -d
