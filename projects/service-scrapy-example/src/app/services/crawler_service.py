from __future__ import annotations

import json
from typing import Any, Mapping

from domain.crawler.config import CrawlerConfig


def get_crawler_config(payload: Mapping[str, Any]) -> CrawlerConfig | None:
    raw_config = payload.get("crawler_config")
    if raw_config is None:
        return None

    if isinstance(raw_config, CrawlerConfig):
        return raw_config

    if isinstance(raw_config, str):
        return CrawlerConfig.from_dict(json.loads(raw_config))

    if isinstance(raw_config, Mapping):
        return CrawlerConfig.from_dict(dict(raw_config))

    raise TypeError("crawler_config must be a mapping or a JSON string")


def build_runner_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    runner_payload = dict(payload)
    config = get_crawler_config(payload)
    if config is not None:
        runner_payload["crawler_config"] = config.model_dump()
    return runner_payload
