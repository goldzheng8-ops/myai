from __future__ import annotations

from application.config.merger import ConfigMerger
from application.config.model import SpiderConfigOverride
from application.config.rules import SPIDER_CONFIG_MERGE_RULES
from core.spider.config import SpiderConfigUnion
from pydantic import TypeAdapter




class SpiderConfigResolver:

    def __init__(
        self,
        merger: ConfigMerger,
    ) -> None:

        self._merger = merger

    def resolve(
        self,
        config: SpiderConfigUnion,
        override: SpiderConfigOverride | None,
    ) -> SpiderConfigUnion:

        if override is None:
            return config

        data = self._merger.merge(
            config,
            override,
            SPIDER_CONFIG_MERGE_RULES,
        )

        return TypeAdapter(
            SpiderConfigUnion,
        ).validate_python(
            data,
        )