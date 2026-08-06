'''DictAccessor
SequenceAccessor
AttributeAccessor
PydanticAccessor
SQLAlchemyAccessor
BeautifulSoupAccessor
PlaywrightAccessor'''
from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence


class ObjectAccessor(ABC):
    """
    Access one level of an object.

    Examples
    --------
    dict["name"]

    list[0]

    object.name
    """

    @abstractmethod
    def supports(
        self,
        value: Any,
    ) -> bool:
        ...

    @abstractmethod
    def access(
        self,
        value: Any,
        key: str,
    ) -> Any:
        ...

class MappingAccessor(ObjectAccessor):

    def supports(self, value: Any) -> bool:
        return isinstance(value, Mapping)

    def access(self, value: Mapping[str, Any], key: str) -> Any:
        return value[key]

class SequenceAccessor(ObjectAccessor):

    def supports(self, value: Any) -> bool:
        return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))

    def access(self, value: Sequence[Any], key: str) -> Any:
        return value[int(key)]

class AttributeAccessor(ObjectAccessor):

    def supports(self, value: Any) -> bool:
        return True

    def access(self, value: Any, key: str) -> Any:
        return getattr(value, key)