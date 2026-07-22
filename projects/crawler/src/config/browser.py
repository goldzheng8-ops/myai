from pydantic import BaseModel, Field

from config.config import BrowserEngine, BrowserWaitUntil
from config.selector.base import SelectorConfig


class BrowserConfig(BaseModel):

    enabled:bool=False

    engine:BrowserEngine=BrowserEngine.PLAYWRIGHT

    wait_until:BrowserWaitUntil=BrowserWaitUntil.NETWORKIDLE

    timeout:int=30000

    scroll:bool=False

    scroll_times:int=0

    click_actions:list[SelectorConfig]=Field(default_factory=list)

    js_scripts:list[str]=Field(default_factory=list)