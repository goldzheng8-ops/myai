from __future__ import annotations
from playwright.async_api import Response
import asyncio
from dataclasses import dataclass, field
from typing import Callable, Literal, cast

from core.request.browser.cookie_sink import BrowserCookieSink
from core.request.downloader.extractor.playwright import PlaywrightCookieExtractor
from core.request.downloader.serializer.playwright import PlaywrightCookieSerializer
from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    ProxySettings,
    async_playwright,
)

from core.lifecycle.protocol import LifecycleParticipant
from core.request.browser.config import BrowserContextConfig, BrowserRuntimeConfig
from core.request.middleware.proxy.config import ProxyConfig
from core.request.middleware.cookie.model import Cookie

ColorScheme = Literal['dark', 'light', 'no-preference', 'null']


@dataclass(slots=True)
class BrowserSessionRuntime:
    session_id: str
    context: BrowserContext
    page: Page

    proxy: ProxyConfig | None = None

    cookie_sink: BrowserCookieSink | None = None

    lock: asyncio.Lock = field(
        default_factory=asyncio.Lock,
    )

    cookie_tasks: set[
        asyncio.Task[None]
    ] = field(
        default_factory=set,
    )
    response_handler: (
        Callable[[Response], None] | None
    ) = None

    async def close(self) -> None:

        if self.response_handler is not None:
            self.context.remove_listener(
                "response",
                self.response_handler,
            )

        tasks = tuple(self.cookie_tasks)

        self.cookie_tasks.clear()

        if tasks:
            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        if not self.page.is_closed():
            await self.page.close()

        await self.context.close()

class BrowserRuntimeManager(LifecycleParticipant):
    """
    Owns the Playwright runtime lifecycle.

    Responsibilities:
    - Playwright lifecycle
    - Browser lifecycle
    - BrowserContext lifecycle
    - logical browser session lifecycle
    - browser-side cookie injection

    This class does not know about:
    - RequestContext
    - RequestDescriptor
    - Framework Middleware
    - Session
    - Downloader
    """

    def __init__(
        self,
        config: BrowserRuntimeConfig,
        context_config: BrowserContextConfig,
    ) -> None:
        self._config = config
        self._context_config = context_config

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

        self._sessions: dict[str, BrowserSessionRuntime] = {}

        self._lock = asyncio.Lock()

    @property
    def config(self) -> BrowserRuntimeConfig:
        return self._config

    async def start(self) -> None:
        """
        Start Playwright and the configured browser.

        Safe to call multiple times.
        """
        async with self._lock:
            if self._browser is not None:
                return

            playwright = await async_playwright().start()

            try:
                browser_type = self._get_browser_type(playwright)

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
        cookie_sink: BrowserCookieSink | None = None,
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

                if (
                    cookie_sink is not None
                    and session.cookie_sink is None
                ):
                    session.cookie_sink = cookie_sink

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
                cookie_sink=cookie_sink,
            )

            self._install_cookie_listener(
                session,
            )

            self._sessions[session_id] = session

            return session

    async def apply_cookies(
        self,
        *,
        session: BrowserSessionRuntime,
        cookies: tuple[Cookie, ...],
        url: str,
    ) -> None:
        """
        Inject framework cookies into the BrowserContext.

        Cookie lifecycle itself belongs to Framework Middleware.
        This method only performs the transport-specific conversion
        and injection into Playwright.
        """
        if not cookies:
            return

        serialized = PlaywrightCookieSerializer.serialize_many(
            cookies,
            url=url,
        )

        if not serialized:
            return

        await session.context.add_cookies(
            list(serialized),
        )

    async def close(self) -> None:
        """
        Close all sessions, Browser and Playwright.
        """
        async with self._lock:
            sessions = tuple(self._sessions.values())
            self._sessions.clear()

            browser = self._browser
            playwright = self._playwright

            self._browser = None
            self._playwright = None

        await asyncio.gather(
            *(session.close() for session in sessions),
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
            device_scale_factor=config.device_scale_factor,
            is_mobile=config.is_mobile,
            has_touch=config.has_touch,
            color_scheme=cast(
                ColorScheme,
                config.color_scheme,
            ),
            java_script_enabled=config.java_script_enabled,
            accept_downloads=config.accept_downloads,
            ignore_https_errors=config.ignore_https_errors,
            extra_http_headers=(
                config.extra_http_headers
                if config.extra_http_headers
                else None
            ),
            storage_state=config.storage_state,
            proxy=self._build_proxy(proxy_config),
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

    @staticmethod
    def _build_proxy(
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

    def _install_cookie_listener(
        self,
        session: BrowserSessionRuntime,
    ) -> None:

        def handler(
            response: Response,
        ) -> None:

            task = asyncio.create_task(
                self._process_response_cookies(
                    session,
                    response,
                )
            )

            session.cookie_tasks.add(task)

            task.add_done_callback(
                session.cookie_tasks.discard,
            )

        session.response_handler = handler

        session.context.on(
            "response",
            handler,
        )


    async def _process_response_cookies(
        self,
        session: BrowserSessionRuntime,
        response: Response,
    ) -> None:

        sink = session.cookie_sink

        if sink is None:
            return

        cookies = await (
            PlaywrightCookieExtractor.extract(
                response,
            )
        )

        if not cookies:
            return

        await sink.update(
            cookies,
        )