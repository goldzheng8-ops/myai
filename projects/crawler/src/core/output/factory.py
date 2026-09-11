from collections.abc import Sequence
from typing import Any

from core.output.config import OutputConfigUnion
from core.output.sink.base import OutputSink
from core.output.sink.csv import CsvOutputSink
from core.output.sink.jsonl import JsonlOutputSink
from core.output.sink.postgres import PostgresOutputSink
from core.output.typing import OutputType


class OutputSinkFactory:

    def create(
        self,
        config: OutputConfigUnion,
    ) -> OutputSink[Any]:

        match config.type:
            case OutputType.JSONL.value:
                return JsonlOutputSink(config)

            case OutputType.CSV.value:
                return CsvOutputSink(config)

            case OutputType.POSTGRES.value:
                return PostgresOutputSink(config)

            case _:
                raise ValueError(
                    f"Unsupported output type: {config.type!r}",
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