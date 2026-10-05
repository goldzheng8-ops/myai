from typing import Any

from core.input.engine import InputEngine
from core.input.loader import DataSourceLoader
from core.input.reader.csv import CsvDataReader
from core.input.reader.excel import ExcelDataReader
from core.input.reader.json import JsonDataReader
from core.input.registry import DataReaderRegistry
from core.input.source import DataFormat
from core.provider.protocol import ProviderResolver
from core.provider.builder import ProviderBuilder



def register_inputs(
    builder: ProviderBuilder,
) -> None:
    builder.add_type(
        CsvDataReader,
    )

    builder.add_type(
        JsonDataReader,
    )

    builder.add_type(
        ExcelDataReader,
    )
    builder.add_type(
        DataSourceLoader,
    )

    builder.add_type(
        InputEngine,
    )
    builder.add_factory(
        DataReaderRegistry,
        create_data_reader_registry,
    )

def create_data_reader_registry(
    resolver: ProviderResolver[Any, Any],
) -> DataReaderRegistry:

    registry = DataReaderRegistry()

    registry.register(
        DataFormat.CSV,
        resolver.resolve(
            CsvDataReader,
        ),
    )

    registry.register(
        DataFormat.JSON,
        resolver.resolve(
            JsonDataReader,
        ),
    )

    registry.register(
        DataFormat.EXCEL,
        resolver.resolve(
            ExcelDataReader,
        ),
    )

    return registry