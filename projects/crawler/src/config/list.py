from config.selector.base import SelectorConfig
from pydantic import BaseModel

class ListConfig(BaseModel):
    selector: SelectorConfig | None = None
    follow_links: bool = False