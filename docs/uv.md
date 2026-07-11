| 功能         | uv 命令                                  |
| ---------- | -------------------------------------- |
| 创建虚拟环境     | `uv venv`                              |
| 安装所有依赖     | `uv sync`                              |
| 添加依赖       | `uv add fastapi`                       |
| 添加开发依赖     | `uv add --dev pytest`                  |
| 删除依赖       | `uv remove fastapi`                    |
| 运行程序       | `uv run python main.py`                |
| 运行 Uvicorn | `uv run uvicorn app.main:app --reload` |
| 运行 pytest  | `uv run pytest`                        |




uv venv
uv sync
uv run python
uv run uvicorn src.app.main:app

uv run uvicorn ...
uv run pytest
RUN uv sync --no-dev