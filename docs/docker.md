# 安装 Docker Desktop
    https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com


# 配置 Docker 镜像
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.1panel.live"
  ]

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