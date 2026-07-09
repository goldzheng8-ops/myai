# 推荐架构（非常重要）
    ⭐ Qwen2.5-VL
    支持：
    3B
    7B
    32B
    72B
    官方说明：
    ✔ multimodal（图像+文本）
    ✔ 支持 agent
    ✔ 支持 browser automation
    ✔ 适配 Ollama 0.7+
    ollama rm qwen2.5:7b
    ollama pull qwen2.5vl:7b
# 安装
    https://ollama.com/download/windows
    下载Windows版本
    ollama -v
    ollama run qwen2.5vl:7b
    ollama list
    ollama show qwen2.5vl:7b
    ollama ps
    ollama serve
    ollama stop qwen3:8b
    ollama stop all
# 安装Ollama适配器
    python -m pip install -U langchain-ollama

    Model                  用途

qwen3:8b               Browser Agent

qwen2.5vl:7b           Vision

gemma3:12b             翻译

llama3.2:3b            快速测试

gpt-oss                Coding


