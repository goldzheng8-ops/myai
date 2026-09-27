from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.request.browser.config import BrowserPageSnapshotConfig
from playwright.async_api import Page


@dataclass(frozen=True, slots=True)
class BrowserPageSnapshot:

    url: str

    title: str

    body_text: str

    html: str | None = None


class BrowserPageSnapshotBuilder(ABC):

    @abstractmethod
    async def build(
        self,
        page: Page,
    ) -> BrowserPageSnapshot:
        raise NotImplementedError

class PlaywrightBrowserPageSnapshotBuilder(
    BrowserPageSnapshotBuilder,
):

    def __init__(
        self,
        config: BrowserPageSnapshotConfig | None = None,
    ) -> None:

        self._config = (
            config
            if config is not None
            else BrowserPageSnapshotConfig()
        )

    async def build(
        self,
        page: Page,
    ) -> BrowserPageSnapshot:

        body_text = await page.locator(
            "body",
        ).inner_text()

        if (
            self._config.max_text_length
            is not None
        ):
            body_text = body_text[
                :self._config.max_text_length
            ]

        html = None

        if self._config.include_html:
            html = await page.content()

        return BrowserPageSnapshot(
            url=page.url,
            title=await page.title(),
            body_text=body_text,
            html=html,
        )