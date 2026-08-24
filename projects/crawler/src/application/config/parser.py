from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol
from pydantic import ValidationError

from application.config.model import ApplicationFileConfig






class ConfigParser(Protocol):
    """
    Parses raw configuration data into
    ApplicationConfig.
    """

    def parse(
        self,
        data: Mapping[str, Any],
    ) -> ApplicationFileConfig:
        ...

class PydanticConfigParser:
    """
    Parses raw configuration data into ApplicationFileConfig.
    """

    def parse(
        self,
        data: Mapping[str, Any],
    ) -> ApplicationFileConfig:

        try:
            return ApplicationFileConfig.model_validate(
                data,
            )

        except ValidationError as exc:
            raise ValueError(
                "Invalid application configuration.",
            ) from exc