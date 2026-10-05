from typing import Any, Mapping, Protocol, Sequence


class ObjectAccessor(Protocol):

    def supports(
        self,
        value: Any,
        key: str,
    ) -> bool:
        ...

    def access(
        self,
        value: Any,
        key: str,
    ) -> Any:
        ...

class MappingAccessor:

    def supports(
        self,
        value: Any,
        key: str,
    ) -> bool:
        return isinstance(value, Mapping)

    def access(
        self,
        value: Any,
        key: str,
    ) -> Any:
        return value[key]

class SequenceAccessor:

    def supports(
        self,
        value: Any,
        key: str,
    ) -> bool:
        return (
            isinstance(value, Sequence)
            and not isinstance(
                value,
                (str, bytes),
            )
            and key.isdigit()
        )

    def access(
        self,
        value: Any,
        key: str,
    ) -> Any:
        return value[int(key)]

class AttributeAccessor:

    def supports(
        self,
        value: Any,
        key: str,
    ) -> bool:
        return hasattr(
            value,
            key,
        )

    def access(
        self,
        value: Any,
        key: str,
    ) -> Any:
        return getattr(
            value,
            key,
        )