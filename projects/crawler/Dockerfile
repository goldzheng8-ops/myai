FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/service/src

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /service

COPY pyproject.toml  uv.lock README.md ./

RUN uv sync --frozen --no-dev --no-install-project

COPY application.yaml ./application.yaml

COPY src ./src

RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "application.main"]

