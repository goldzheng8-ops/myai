from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(slots=True, frozen=True)
class ResolveExpression(ABC):

    @property
    @abstractmethod
    def cache_key(self) -> str:
        ...


@dataclass(slots=True, frozen=True)
class DotPathExpression(ResolveExpression):

    path: str

    @property
    def cache_key(self) -> str:
        return self.path

@dataclass(slots=True, frozen=True)
class JsonPathExpression(ResolveExpression):

    path: str

    @property
    def cache_key(self) -> str:
        return f"jsonpath:{self.path}"

@dataclass(slots=True, frozen=True)
class JMESExpression(ResolveExpression):

    expression: str

    @property
    def cache_key(self) -> str:
        return f"jmes:{self.expression}"

'''
JsonPointerExpression

JsonPathExpression

JMESExpression
'''