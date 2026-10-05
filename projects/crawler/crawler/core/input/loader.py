from collections.abc import Iterable

from core.input.record import DataRecord
from core.input.registry import DataReaderRegistry
from core.input.source import DataSource


class DataSourceLoader:

    def __init__(
        self,
        readers: DataReaderRegistry,
    ) -> None:
        self._readers = readers

    def read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        reader = self._readers.get(
            source.format,
        )

        return reader.read(
            source,
        )