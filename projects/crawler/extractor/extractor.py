from __future__ import annotations

from typing import Any

from adapters.base import ResponseAdapter
from config.config import ExtractFieldConfig
from selector.engine import SelectorEngine
from transform.engine import TransformEngine


class ExtractorEngine:
    """
    负责协调 SelectorEngine 和 TransformEngine，
    完成整个页面的数据抽取。
    """

    def __init__(
        self,
        selector_engine: SelectorEngine,
        transform_engine: TransformEngine,
    ) -> None:
        self.selector_engine = selector_engine
        self.transform_engine = transform_engine

    def extract(
        self,
        adapter: ResponseAdapter,
        fields: list[ExtractFieldConfig],
    ) -> dict[str, Any]:
        """
        提取整个页面。

        Args:
            adapter: ResponseAdapter
            fields: 所有字段配置

        Returns:
            dict[str, Any]
        """

        result: dict[str, Any] = {}

        for field in fields:
            try:
                result[field.name] = self._extract_field(
                    adapter,
                    field,
                )

            except Exception:

                if field.required:
                    raise

                result[field.name] = field.default

        return result

    def _extract_field(
        self,
        adapter: ResponseAdapter,
        field: ExtractFieldConfig,
    ) -> Any:
        """
        提取单个字段。
        """

        value = self.selector_engine.select(
            adapter,
            field.selector,
        )

        if value is None:

            if field.required:
                raise ValueError(
                    f"Required field '{field.name}' not found."
                )

            return field.default

        if field.transforms:

            value = self.transform_engine.execute(
                value,
                field.transforms,
            )

        return value