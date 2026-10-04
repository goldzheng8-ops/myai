from collections.abc import Iterable

from core.input.loader import DataSourceLoader
from core.input.record import DataRecord
from core.input.source import DataSource


class InputEngine:

    def __init__(
        self,
        loader: DataSourceLoader,
    ) -> None:
        self._loader = loader

    def read(
        self,
        source: DataSource,
    ) -> Iterable[DataRecord]:
        return self._loader.read(
            source,
        )