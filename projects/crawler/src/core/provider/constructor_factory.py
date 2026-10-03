import inspect
from typing import Any, Generic, TypeVar, get_type_hints

from core.provider.base import ProviderResolver


T = TypeVar("T")


class ConstructorFactory(Generic[T]):

    def __init__(
        self,
        implementation: type[T],
    ) -> None:

        self._implementation = implementation

    def __call__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> T:

        signature = inspect.signature(
            self._implementation.__init__,
        )

        type_hints = get_type_hints(
            self._implementation.__init__,
        )

        args: list[Any] = []
        kwargs: dict[str, Any] = {}

        for parameter in signature.parameters.values():

            if parameter.name == "self":
                continue

            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            # 有默认值的参数交给 constructor 自己处理。
            if (
                parameter.default
                is not inspect.Parameter.empty
            ):
                continue

            annotation = type_hints.get(
                parameter.name,
            )

            if annotation is None:

                raise TypeError(
                    f"Cannot resolve constructor parameter "
                    f"{self._implementation.__name__}"
                    f".{parameter.name!s}: "
                    f"missing type annotation."
                )

            dependency = resolver.resolve(
                annotation,
            )

            if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
                args.append(dependency)
            else:
                kwargs[parameter.name] = dependency

        return self._implementation(
            *args,
            **kwargs,
        )