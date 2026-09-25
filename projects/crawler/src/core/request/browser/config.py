from playwright.async_api import StorageState
from pydantic import Field
from typing import Literal
from core.typing.config import BaseConfig
from pathlib import Path

class BrowserContextConfig(BaseConfig):
    """
    headless
    browser executable
    browser type
    launch args
    属于 Browser / BrowserLauncher 层。、

    Configuration used to create a Playwright BrowserContext.
    """

    user_agent: str | None = None

    locale: str | None = None

    timezone_id: str | None = None

    viewport_width: int | None = None

    viewport_height: int | None = None

    device_scale_factor: float | None = None

    is_mobile: bool = False

    has_touch: bool = False

    color_scheme: str | None = None

    java_script_enabled: bool = True

    accept_downloads: bool = True

    ignore_https_errors: bool = False

    extra_http_headers: dict[str, str] = Field(
        default_factory=dict,
    )

    storage_state: str | StorageState | Path | None = None

class BrowserRuntimeConfig(BaseConfig):

    browser: Literal[
        "chromium",
        "firefox",
        "webkit",
    ] = "chromium"

    headless: bool = True