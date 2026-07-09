FROM python:3.12-slim

WORKDIR /app

# Install OS dependencies required by Playwright and Python package builds
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libpq-dev \
       libssl-dev \
       libffi-dev \
       ca-certificates \
       wget \
       fonts-liberation \
       libatk1.0-0 \
       libatk-bridge2.0-0 \
       libgtk-3-0 \
       libx11-xcb1 \
       libxcomposite1 \
       libxrandr2 \
       libasound2 \
       libgbm1 \
       libpangocairo-1.0-0 \
       libxss1 \
       libnss3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (downloads browser binaries)
RUN python -m playwright install --with-deps

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]