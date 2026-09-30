from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.request.browser.config import BrowserPageSnapshotConfig
from playwright.async_api import Page

@dataclass(slots=True)
class BrowserPageRuntimeState:
    status_code: int | None = None
    content_type: str | None = None

    last_main_document_url: str | None = None
    last_main_document_status: int | None = None
    last_main_document_method: str | None = None
    last_main_document_resource: str | None = None

    navigation_count: int = 0

@dataclass(frozen=True, slots=True)
class BrowserPageSnapshot:

    url: str
    title: str
    body_text: str

    html: str | None = None

    status_code: int | None = None
    content_type: str | None = None

    has_body: bool = False
    has_forms: bool = False
    has_inputs: bool = False
    has_iframes: bool = False


class BrowserPageSnapshotBuilder(ABC):

    @abstractmethod
    async def build(
        self,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
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
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageSnapshot:

        has_body = (
            await page.locator("body").count()
            > 0
        )

        body_text = ""

        if has_body:
            body_text = await page.locator(
                "body",
            ).inner_text()

        if self._config.max_text_length is not None:
            body_text = body_text[
                :self._config.max_text_length
            ]

        html: str | None = None

        if self._config.include_html:
            html = await page.content()

        has_forms = (
            await page.locator("form").count()
            > 0
        )

        has_inputs = (
            await page.locator(
                "input, textarea, select, button",
            ).count()
            > 0
        )

        has_iframes = (
            await page.locator("iframe").count()
            > 0
        )

        return BrowserPageSnapshot(
            url=page.url,
            title=await page.title(),
            body_text=body_text,
            html=html,
            status_code=runtime_state.status_code,
            content_type=runtime_state.content_type,
            has_body=has_body,
            has_forms=has_forms,
            has_inputs=has_inputs,
            has_iframes=has_iframes,
        )