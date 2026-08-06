
from typing import TypeVar

from core.runtime.expression import ResolveExpression


ExpressionT = TypeVar(
    "ExpressionT",
    bound=ResolveExpression,
)