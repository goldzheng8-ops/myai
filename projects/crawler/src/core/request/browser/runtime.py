import asyncio
from dataclasses import dataclass, field

from core.request.middleware.proxy.config import ProxyConfig
from playwright.async_api import (
    BrowserContext,
    Page,
)


@dataclass(slots=True)
class BrowserSessionRuntime:

    session_id: str

    context: BrowserContext

    page: Page

    proxy: ProxyConfig | None = None

    lock: asyncio.Lock = field(
        default_factory=asyncio.Lock,
    )


    pages: dict[str, Page] = field(
        default_factory=dict,
    )

    def get_page(
        self,
        page_id: str,
    ) -> Page | None:

        return self.pages.get(page_id)

    async def get_or_create_page(
        self,
        page_id: str,
    ) -> Page:

        page = self.pages.get(page_id)

        if page is not None:
            return page

        page = await self.context.new_page()

        self.pages[page_id] = page

        return page

    async def close_page(
        self,
        page_id: str,
    ) -> None:

        page = self.pages.pop(
            page_id,
            None,
        )

        if page is None:
            return

        await page.close()

    async def close(self) -> None:

        self.pages.clear()

        await self.context.close()