from collections.abc import Iterable
from typing import Protocol
from abc import ABC, abstractmethod

from core.input.record import DataRecord
from core.input.source import DataFormat, DataSource


class DataReader(Protocol):

    def read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        ...

class BaseDataReader(ABC):

    format: DataFormat

    def read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        self._validate_source(source)

        yield from self._read(source)

    @abstractmethod
    def _read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        raise NotImplementedError

    def _validate_source(
        self,
        source: DataSource,
    ) -> None:
        requested_format = DataFormat(source.format)

        if requested_format is not self.format:
            raise ValueError(
                f"{type(self).__name__} does not support "
                f"data format {source.format!r}.",
            )