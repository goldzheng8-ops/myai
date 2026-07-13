FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/service/src

RUN pip install --no-cache-dir uv

WORKDIR /service

COPY pyproject.toml  README.md ./

RUN uv sync --no-dev 

COPY src ./src

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]