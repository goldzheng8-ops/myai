from core.input.reader.base import DataReader
from core.input.source import DataFormat
from core.registry import Registry


class DataReaderRegistry(
    Registry[
        DataFormat,
        DataReader,
    ],
):
    pass