from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

import yaml


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
    """
    Loads application configuration from YAML.
    """

    def load(
        self,
        source: str | Path,
    ) -> dict[str, Any]:

        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file does not exist: "
                f"{path}",
            )

        if not path.is_file():
            raise ValueError(
                f"Configuration path is not a file: "
                f"{path}",
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = yaml.safe_load(file)

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise TypeError(
                "Application configuration root "
                "must be a mapping.",
            )

        return data