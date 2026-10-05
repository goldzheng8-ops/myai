from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from application.config.model import ApplicationConfig
from pydantic import TypeAdapter
import yaml
from pydantic import ValidationError


class ConfigLoadError(Exception):
    pass

class ConfigLoader(Protocol):
    """
    Loads raw application configuration.
    """

    def load(
        self,
        source: str | Path,
    ) -> dict[str, Any]:
        ...


class YamlConfigLoader:

    def __init__(self) -> None:
        self._adapter = TypeAdapter(
            ApplicationConfig,
        )

    def load(
        self,
        path: str | Path,
    ) -> ApplicationConfig:

        path = Path(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data: Any = yaml.safe_load(file)

        return self._adapter.validate_python(data)

    def load_text(
        self,
        text: str,
    ) -> ApplicationConfig:

        try:
            data: Any = yaml.safe_load(text)

            return self._adapter.validate_python(
                data,
            )

        except yaml.YAMLError as exc:
            raise ConfigLoadError(
                "Invalid YAML configuration"
            ) from exc

        except ValidationError as exc:
            raise ConfigLoadError(
                "Invalid spider configuration"
            ) from exc

    def dump(
        self,
        config: ApplicationConfig,
        path: str | Path,
    ) -> None:

        path = Path(path)

        data = config.model_dump(
            mode="json",
            exclude_none=True,
        )

        text = yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False,
        )

        path.write_text(
            text,
            encoding="utf-8",
        )