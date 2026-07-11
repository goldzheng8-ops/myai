from __future__ import annotations

import inspect
import os
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPIDER_PROJECT_ROOT = PROJECT_ROOT / "src" / "domain" / "crawler"


def resolve_spider_class(spider_name: str) -> type[scrapy.Spider]:
    module_name = f"test1.spiders.{spider_name}"
    module = import_module(module_name)

    for _, obj in inspect.getmembers(module, inspect.isclass):
        if (
            issubclass(obj, scrapy.Spider)
            and obj is not scrapy.Spider
            and obj.__module__ == module.__name__
        ):
            return obj

    raise ValueError(f"No Scrapy spider found for {spider_name}")


def run_scrapy_job(payload: dict[str, Any]) -> dict[str, Any]:
    task_id = payload["task_id"]
    spider_name = payload["spider"]
    target_url = payload.get("url")

    spider_cls = resolve_spider_class(spider_name)

    original_cwd = Path.cwd()
    project_root = PROJECT_ROOT
    spider_project_root = SPIDER_PROJECT_ROOT

    if str(spider_project_root) not in sys.path:
        sys.path.insert(0, str(spider_project_root))

    os.chdir(project_root)
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "test1.settings")
    try:
        settings = get_project_settings()
        settings.set("LOG_LEVEL", settings.get("LOG_LEVEL", "INFO"))

        if target_url:
            class DynamicSpider(spider_cls):  # type: ignore[valid-type, misc]
                name = f"{spider_cls.name}-{task_id}"
                start_urls = [target_url]

            runner_spider = DynamicSpider
        else:
            runner_spider = spider_cls

        process = CrawlerProcess(settings)
        process.crawl(runner_spider)
        process.start()

        return {
            "task_id": task_id,
            "status": "completed",
            "spider": spider_name,
            "message": f"Spider {spider_name} completed",
        }
    except Exception as exc:  # pragma: no cover - defensive branch
        return {
            "task_id": task_id,
            "status": "failed",
            "spider": spider_name,
            "error": str(exc),
        }
    finally:
        os.chdir(original_cwd)
