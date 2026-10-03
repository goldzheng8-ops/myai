from typing import Any

from core.runtime.expression import DotPathExpression, ResolveExpression, TemplateExpression


class ResolveExpressionParser:

    def parse(
        self,
        value: Any,
    ) -> ResolveExpression | None:

        if not isinstance(value, str):
            return None

        value = value.strip()

        if value.startswith("$."):
            return DotPathExpression(
                value[2:],
            )

        if "{{" in value:
            return TemplateExpression(
                value,
            )

        return None