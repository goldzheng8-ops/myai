from fastapi.testclient import TestClient

from app.main import app
from domain.crawler.config import CrawlerConfig
from domain.crawler.executors import ApiExecutor, PlaywrightExecutor, ScrapyExecutor, select_executor
from domain.crawler.templates import build_template_spider


def test_config_model_and_template_building():
    config = CrawlerConfig.from_dict(
        {
            "request": {"url": "https://example.com"},
            "list": {"selector": "article"},
            "extract": {
                "fields": {
                    "title": {"selector": "h2::text", "type": "text"},
                }
            },
        }
    )

    spider_cls = build_template_spider(config, task_id="task-1")

    assert spider_cls.name.startswith("TemplateListSpider")
    assert spider_cls.start_urls == ["https://example.com"]
    assert spider_cls.crawler_config.request.url == "https://example.com"


def test_select_executor_by_config():
    default_executor = select_executor(CrawlerConfig.from_dict({"request": {"url": "https://example.com"}}))
    browser_executor = select_executor(
        CrawlerConfig.from_dict({"request": {"url": "https://example.com"}, "browser": {"enabled": True}})
    )
    api_executor = select_executor(
        CrawlerConfig.from_dict({"request": {"url": "https://example.com/api"}, "template": "api"})
    )

    assert isinstance(default_executor, ScrapyExecutor)
    assert isinstance(browser_executor, PlaywrightExecutor)
    assert isinstance(api_executor, ApiExecutor)


def test_submit_crawl_task_accepts_crawler_config(monkeypatch):
    calls = []

    def fake_runner(payload):
        calls.append(payload)
        return {
            "task_id": payload["task_id"],
            "status": "completed",
            "spider": payload["spider"],
            "message": "ok",
        }

    monkeypatch.setattr("app.main.run_scrapy_job", fake_runner)

    client = TestClient(app)
    response = client.post(
        "/crawl/tasks",
        json={
            "spider": "template",
            "crawler_config": {
                "request": {"url": "https://example.com"},
                "list": {"selector": "article"},
            },
        },
    )

    assert response.status_code == 202
    assert calls[0]["crawler_config"]["request"]["url"] == "https://example.com"
