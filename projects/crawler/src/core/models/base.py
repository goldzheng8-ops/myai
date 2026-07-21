from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )