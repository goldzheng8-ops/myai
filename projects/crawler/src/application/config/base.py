from pydantic import ConfigDict

from core.typing.config import BaseConfig

class ApplicationConfigBase(BaseConfig):
    """
    Base configuration model for the application layer.

    Application configuration is immutable after validation.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        frozen=True,
    )
