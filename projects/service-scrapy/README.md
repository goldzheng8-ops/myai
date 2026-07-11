
# 启动服务：
uvicorn app.main:app --host 0.0.0.0 --port 8001
# 提交任务：
curl -X POST http://127.0.0.1:8001/crawl/tasks \
  -H "Content-Type: application/json" \
  -d '{"spider":"example","url":"https://example.com"}'
# 查询任务状态
curl http://127.0.0.1:8001/crawl/tasks/{task_id}


###########################################################################
docker build -t service-scrapy:test .
docker run --rm -p 8001:8001 --name service-scrapy-test service-scrapy:test

docker build -t service-scrapy:test .
docker run --rm -p 8001:8001 service-scrapy:test