

from config.request import RequestConfig
from config.request_merge import RequestMergeConfig
from enums.merge_policy import MergePolicy
from runtime.discovery_descriptor import RequestDescriptor


from copy import deepcopy
from dataclasses import dataclass

from abc import ABC, abstractmethod
from typing import Any, TypeVar
from typing import Generic, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class BaseMerger(Generic[T], ABC):

    @classmethod
    def merge(
        cls,
        parent: T,
        child: T | None,
        policy: MergePolicy,
    ) -> T:

        if child is None:
            return parent

        match policy:

            case MergePolicy.IGNORE:
                return parent

            case MergePolicy.REPLACE:
                return cls.replace(parent, child)

            case MergePolicy.MERGE:
                return cls.do_merge(parent, child)

            case MergePolicy.REMOVE:
                return cls.remove(parent)

        raise ValueError(policy)

    @classmethod
    @abstractmethod
    def do_merge(
        cls,
        parent: T,
        child: T,
    ) -> T:
        ...

    @classmethod
    @abstractmethod
    def replace(
        cls,
        parent: T,
        child: T,
    ) -> T:
        ...

    @classmethod
    @abstractmethod
    def remove(
        cls,
        parent: T,
    ) -> T:
        ...

@dataclass(frozen=True, slots=True)
class MergeRule:

    field: str

    merger: type[BaseMerger[Any]]

    policy: MergePolicy

class MappingMerger(
    BaseMerger[dict[K, V]]
):

    @classmethod
    def do_merge(
        cls,
        parent: dict[K, V],
        child: dict[K, V],
    ) -> dict[K, V]:

        result = deepcopy(parent)
        result.update(deepcopy(child))
        return result

    @classmethod
    def replace(
        cls,
        parent: dict[K, V],
        child: dict[K, V],
    ) -> dict[K, V]:

        return deepcopy(child)

    @classmethod
    def remove(
        cls,
        parent: dict[K, V],
    ) -> dict[K, V]:

        return {}

class ValueMerger(
    BaseMerger[T]
):

    @classmethod
    def do_merge(
        cls,
        parent: T,
        child: T,
    ) -> T:

        return child

    @classmethod
    def replace(
        cls,
        parent: T,
        child: T,
    ) -> T:

        return child

    @classmethod
    def remove(
        cls,
        parent: T,
    ) -> T:
        raise NotImplementedError(
            "ValueMerger does not support REMOVE."
        )

class RequestMerger:

    def __init__(
        self,
        config: RequestMergeConfig | None = None,
    ):
        self._config = config or RequestMergeConfig()

    def merge(
        self,
        parent: RequestConfig,
        descriptor: RequestDescriptor,
    ) -> RequestConfig:

        request = parent.model_copy(deep=True)

        request.url = descriptor.url

        for rule in self._config.rules:

            parent_value = getattr(
                request,
                rule.field,
            )

            child_value = getattr(
                descriptor,
                rule.field,
            )

            merged = rule.merger.merge(
                parent_value,
                child_value,
                rule.policy,
            )

            setattr(
                request,
                rule.field,
                merged,
            )

        return request