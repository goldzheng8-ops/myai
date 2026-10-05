from collections.abc import Sequence
from typing import Any

from core.output.config import BinaryFileOutputConfig, OutputConfigUnion, StorageConfigUnion
from core.output.filename import DownloadFilenameResolver
from core.output.sink.base import OutputSink
from core.output.sink.binary_file import BinaryFileOutputSink
from core.output.sink.csv import CsvOutputSink
from core.output.sink.json_file import JsonFileOutputSink
from core.output.sink.jsonl import JsonlOutputSink
from core.output.sink.postgres import PostgresOutputSink
from core.output.storage.base import Storage
from core.output.storage.local import LocalFileStorage
from core.output.storage.s3 import S3Storage
from core.output.typing import OutputType
from core.template.manager.base import TemplateManager
from core.output.typing import StorageType

class StorageFactory:

    def create(
        self,
        config: StorageConfigUnion,
    ) -> Storage:

        match config.type:

            case StorageType.LOCAL:
                return LocalFileStorage(
                    directory=config.directory,
                )

            case StorageType.S3:
                return S3Storage(
                    config=config
                )

            case _:
                raise ValueError(
                    f"Unsupported storage type: "
                    f"{config.type!r}",
                )

class DownloadFilenameResolverFactory:

    def __init__(
        self,
        template_manager: TemplateManager,
    ) -> None:
        self._template_manager = template_manager

    def create(
        self,
        config: BinaryFileOutputConfig,
    ) -> DownloadFilenameResolver:

        return DownloadFilenameResolver(
            template_manager=self._template_manager,
            template=config.filename,
        )
class OutputSinkFactory:

    def __init__(
        self,
        storage_factory: StorageFactory,
        filename_resolver_factory: (
            DownloadFilenameResolverFactory
        ),
    ) -> None:
        self._storage_factory = (
            storage_factory
        )
        self._filename_resolver_factory = (
            filename_resolver_factory
        )
        
    def create(
        self,
        config: OutputConfigUnion,
    ) -> OutputSink[Any]:

        match config.type:
            case OutputType.JSONL.value:
                return JsonlOutputSink(config)

            case OutputType.JSON_FILE.value:
                return JsonFileOutputSink(config)

            case OutputType.CSV.value:
                return CsvOutputSink(config)

            case OutputType.POSTGRES.value:
                return PostgresOutputSink(config)

            case OutputType.BINARY_FILE.value:
                return self._create_binary_file(
                    config,
                )

            case _:
                raise ValueError(
                    f"Unsupported output type: "
                    f"{config.type!r}",
                )

    def _create_binary_file(
        self,
        config: BinaryFileOutputConfig,
    ) -> BinaryFileOutputSink:

        storage = self._storage_factory.create(
            config.storage,
        )

        filename_resolver = (
            self._filename_resolver_factory.create(
                config,
            )
        )

        return BinaryFileOutputSink(
            config=config,
            filename_resolver=filename_resolver,
            storage=storage,
        )
    
    def create_all(
        self,
        configs: Sequence[
            OutputConfigUnion
        ],
    ) -> dict[str, OutputSink[Any]]:

        outputs: dict[str, OutputSink[Any]] = {}

        for config in configs:

            if config.name in outputs:
                raise ValueError(
                    "Duplicate outputsink name: "
                    f"{config.name!r}",
                )

            outputs[config.name] = self.create(
                config,
            )

        return outputs