from config.selector.base import SelectorConfig
from pydantic import BaseModel

class DetailConfig(BaseModel):
    enabled: bool = False
    selector: SelectorConfig | None = None
    url_field: str | None = None