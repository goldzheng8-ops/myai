FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/service/src

RUN pip install --no-cache-dir uv

WORKDIR /service

COPY pyproject.toml  README.md ./

RUN uv sync --no-dev 

COPY src ./src

EXPOSE 8002

CMD ["uv", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]