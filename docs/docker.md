# 安装 Docker Desktop
    https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com


# 配置 Docker 镜像源
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.1panel.live"
  ]

# 管理 Docker 镜像
docker pull mcr.microsoft.com/playwright/python:v1.60.0-jammy
docker save -o playwright-python-v1.60.0-jammy.tar mcr.microsoft.com/playwright/python:v1.60.0-jammy
docker load -i playwright-python-v1.60.0-jammy.tar

# 建立 Base Image
dockerfile:
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy
RUN uv pip install \
    playwright \
    fastapi \
    uvicorn
docker build -t goldzheng/playwright-base .

# goldzheng/scrapy-base

Python
uv
Scrapy
lxml
libxml2
libxslt
curl

# goldzheng/playwright-base

Playwright
Chromium
Firefox
WebKit
uv
git

# goldzheng/python-base

Python 3.12
uv
git
curl
vim
build-essential
ca-certificates
tzdata


| 对比          | Jammy  | Slim   | Alpine       |
| ----------- | ------ | ------ | ------------ |
| 基础          | Ubuntu | Debian | Alpine Linux |
| libc        | glibc  | glibc  | musl         |
| 镜像大小        | 大      | 中      | 最小           |
| 软件兼容性       | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐   | ⭐⭐           |
| apt         | ✅      | ✅      | ❌（使用 `apk`）  |
| Python 科学计算 | 很好     | 很好     | 容易踩坑         |
| Playwright  | ✅      | ✅      | 很麻烦          |
| Scrapy      | ✅      | ✅      | 有时需要编译依赖     |

Windows
│
├── Ollama（宿主机）
│    ├── qwen3
│    ├── deepseek
│    └── embedding model
│
└── Docker Desktop
     ├── Open WebUI
     ├── n8n
     ├── PostgreSQL
     ├── Redis
     ├── Qdrant
     ├── MinIO
     ├── SearXNG（以后）
     ├── Flowise（以后）
     └── FastAPI（你的项目）
现在的默认访问入口
n8n: http://localhost:5678
Open WebUI: http://localhost:3000
Qdrant: http://localhost:6333
MinIO: http://localhost:9000
PostgreSQL: localhost:5432
Grafana：http://localhost:3001


docker images
docker compose up -d
docker compose up -d qdrant
docker compose ps
docker compose logs -f
docker compose logs -f open-webui
退出日志：
Ctrl + C
不会停止容器。

docker build -t scrapy-service .
docker run -p 8001:8001 scrapy-service