import asyncio
from typing import Literal, cast

from core.lifecycle.protocol import LifecycleParticipant
from core.request.browser.config import BrowserContextConfig, BrowserRuntimeConfig
from core.request.browser.runtime import BrowserSessionRuntime
from core.request.middleware.proxy.config import ProxyConfig
from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    ProxySettings,
    Playwright,
    async_playwright,
)

ColorScheme = Literal['dark', 'light', 'no-preference', 'null']

class BrowserRuntimeManager(
    LifecycleParticipant,
):

    def __init__(
        self,
        config: BrowserRuntimeConfig,
        context_config: BrowserContextConfig,
    ) -> None:

        self._config = config
        self._context_config = context_config

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

        self._sessions: dict[
            str,
            BrowserSessionRuntime,
        ] = {}

        self._lock = asyncio.Lock()

    @property
    def config(
        self,
    ) -> BrowserRuntimeConfig:

        return self._config

    async def start(self) -> None:

        async with self._lock:

            if self._browser is not None:
                return

            playwright = (
                await async_playwright().start()
            )

            try:

                browser_type = (
                    self._get_browser_type(
                        playwright,
                    )
                )

                browser = await browser_type.launch(
                    headless=self.config.headless,
                )

            except Exception:

                await playwright.stop()

                raise

            self._playwright = playwright
            self._browser = browser

    async def get_session(
        self,
        *,
        session_id: str,
        proxy: ProxyConfig | None = None,
    ) -> BrowserSessionRuntime:
        await self.start()
        async with self._lock:

            session = self._sessions.get(
                session_id,
            )

            if session is not None:

                if not self._same_proxy(
                    session.proxy,
                    proxy,
                ):
                    raise RuntimeError(
                        "Browser session proxy cannot "
                        "be changed after creation: "
                        f"{session_id!r}",
                    )

                return session

            context = await self._create_context(
                context_config=self._context_config,
                proxy_config=proxy,
            )

            try:

                page = await context.new_page()

            except Exception:

                await context.close()

                raise

            session = BrowserSessionRuntime(
                session_id=session_id,
                context=context,
                page=page,
                proxy=proxy,
            )

            self._sessions[session_id] = session

            return session

    async def close(self) -> None:

        async with self._lock:

            sessions = tuple(
                self._sessions.values(),
            )

            self._sessions.clear()

            browser = self._browser
            playwright = self._playwright

            self._browser = None
            self._playwright = None

        await asyncio.gather(
            *(
                session.close()
                for session in sessions
            ),
            return_exceptions=True,
        )

        if browser is not None:
            await browser.close()

        if playwright is not None:
            await playwright.stop()


    async def _create_context(
        self,
        context_config: BrowserContextConfig,
        proxy_config: ProxyConfig | None = None,
    ) -> BrowserContext:

        browser = self._require_browser()
        config = context_config
        
        return await browser.new_context(
            user_agent=config.user_agent,
            locale=config.locale,
            timezone_id=config.timezone_id,
            viewport=(
                {
                    "width": config.viewport_width,
                    "height": config.viewport_height,
                }
                if (
                    config.viewport_width is not None
                    and config.viewport_height is not None
                )
                else None
            ),
            device_scale_factor=(
                config.device_scale_factor
            ),
            is_mobile=config.is_mobile,
            has_touch=config.has_touch,
            color_scheme=cast(ColorScheme,config.color_scheme),
            java_script_enabled=config.java_script_enabled,
            accept_downloads=config.accept_downloads,
            ignore_https_errors=config.ignore_https_errors,
            extra_http_headers=(
                config.extra_http_headers
                if config.extra_http_headers
                else None
            ),
            storage_state=config.storage_state,
            proxy=self._build_proxy(proxy_config)
        )
    def _get_browser_type(
        self,
        playwright: Playwright,
    ) -> BrowserType:

        if self.config.browser == "chromium":
            return playwright.chromium

        if self.config.browser == "firefox":
            return playwright.firefox

        return playwright.webkit

    def _build_proxy(
        self,
        proxy_config: ProxyConfig | None = None,
    ) -> ProxySettings | None:

        if proxy_config is None:
            return None

        result: ProxySettings = {
            "server": proxy_config.url,
        }

        if proxy_config.username is not None:
            result["username"] = proxy_config.username

        if proxy_config.password is not None:
            result["password"] = proxy_config.password

        return result

    @staticmethod
    def _same_proxy(
        left: ProxyConfig | None,
        right: ProxyConfig | None,
    ) -> bool:

        if left is None or right is None:
            return left is right

        return (
            left.url == right.url
            and left.username == right.username
            and left.password == right.password
            and left.country == right.country
        )

    def _require_browser(self) -> Browser:
        browser = self._browser

        if browser is None:
            raise RuntimeError(
                "BrowserRuntimeManager is not started.",
            )

        return browser