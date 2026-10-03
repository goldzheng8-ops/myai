from typing import Any

from core.runtime.context import RuntimeContext
from core.template.manager.default import TemplateManager
from core.runtime.expression import TemplateExpression
from core.runtime.strategy.base import ResolveStrategy

class TemplateStrategy(
    ResolveStrategy[
        TemplateExpression
    ],
):

    expression_type = TemplateExpression

    def __init__(
        self,
        manager: TemplateManager,
    ) -> None:
        self._manager = manager

    def resolve(
        self,
        context: RuntimeContext,
        expression: TemplateExpression,
    ) -> Any:

        return self._manager.render(
            expression.source,
            context.as_mapping(),
        )