from typing import Any

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.request.browser.detector.captcha import CaptchaDetector
from core.request.browser.detector.access_denied import AccessDeniedDetector
from core.request.browser.detector.cloudflare_challenge import CloudflareChallengeDetector
from core.request.browser.detector.login_required import LoginRequiredDetector
from core.request.browser.detector.normal import NormalPageDetector
from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.detector.turnstile_challenge import TurnstileChallengeDetector
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.interaction.base import BrowserInteractionEngine
from core.request.browser.interaction.playwright import PlaywrightBrowserInteractionEngine
from core.request.browser.executor.registry import BrowserActionExecutorRegistry
from core.request.browser.intervention.base import HumanInterventionEngine
from core.request.downloader.aria2.client import Aria2Client
from core.request.downloader.aria2.launcher import Aria2ProcessLauncher
from core.request.downloader.aria2.monitor import Aria2DownloadMonitor
from core.request.downloader.aria2.options import Aria2OptionsBuilder
from core.request.downloader.factory import build_aria2_downloader_factory, build_scrapy_downloader_factory, build_httpx_downloader_factory, build_playwright_downloader_factory
from core.request.downloader.manager import DownloaderManager
from core.request.typing import DownloaderType
from core.request.downloader.registry import DownloaderRegistry
from core.request.browser.executor.navigation import NavigationActionExecutor
from core.request.browser.executor.locator import LocatorActionExecutor
from core.request.browser.executor.input import InputActionExecutor
from core.request.browser.executor.selection import SelectionActionExecutor
from core.request.browser.executor.check import CheckActionExecutor
from core.request.browser.executor.keyboard import KeyboardActionExecutor
from core.request.browser.executor.file import FileActionExecutor
from core.request.browser.executor.wait import WaitActionExecutor
from core.request.browser.executor.evaluate import EvaluateActionExecutor

def register_downloaders(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    builder.add_factory(
        BrowserInteractionEngine,
        lambda resolver: PlaywrightBrowserInteractionEngine(
            inspector=resolver.resolve(
                BrowserPageInspector,
            ),
            human_intervention=resolver.resolve(
                HumanInterventionEngine,
            ),
            executor_registry=resolver.resolve(
                BrowserActionExecutorRegistry,
            ),
        ),
    )
    builder.add_factory(
        Aria2ProcessLauncher,
        lambda resolver: Aria2ProcessLauncher(
            rpc_url=config.aria2.rpc_url,
            executable=config.aria2.executable,
            rpc_secret=config.aria2.rpc_secret,
        ),
    )
    builder.add_factory(
        Aria2Client,
        lambda resolver: Aria2Client(
            rpc_url=config.aria2.rpc_url,
            rpc_secret=config.aria2.rpc_secret,
            timeout=config.aria2.rpc_timeout,
        ),
    )

    builder.add_factory(
        Aria2DownloadMonitor,
        lambda resolver: Aria2DownloadMonitor(
            client=resolver.resolve(
                Aria2Client,
            ),
            poll_interval=config.aria2.poll_interval,
            timeout=config.aria2.monitor_timeout,
        ),
    )

    builder.add_factory(
        Aria2OptionsBuilder,
        lambda resolver: Aria2OptionsBuilder(

        ),
    )

    builder.add_factory(
        DownloaderManager,
        lambda resolver: DownloaderManager(
            registry=resolver.resolve(
                DownloaderRegistry,
            ),
            lifecycle=resolver.resolve(
                LifecycleManager,
            ),
        ),
    )
    
    builder.add_factory(
        DownloaderRegistry,
        lambda resolver: create_downloader_registry(
            resolver,
        ),
    )

def create_downloader_registry(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderRegistry:

    registry = DownloaderRegistry()

    registry.register(
        DownloaderType.HTTPX,
        build_httpx_downloader_factory(
            resolver,
        ),
    )

    registry.register(
        DownloaderType.SCRAPY,
        build_scrapy_downloader_factory(
            resolver,
        ),
    )

    registry.register(
        DownloaderType.PLAYWRIGHT,
        build_playwright_downloader_factory(
            resolver,
        ),
    )
    registry.register(
        DownloaderType.ARIA2,
        build_aria2_downloader_factory(
            resolver,
        ),
    )

    return registry

def create_action_executor_registry(
    resolver: ProviderResolver[Any, Any],
) -> BrowserActionExecutorRegistry:

    registry = BrowserActionExecutorRegistry()

    registry.register(
        "navigation",
        NavigationActionExecutor(),
    )

    registry.register(
        "locator",
        LocatorActionExecutor(),
    )

    registry.register(
        "input",
        InputActionExecutor(),
    )

    registry.register(
        "selection",
        SelectionActionExecutor(),
    )

    registry.register(
        "check",
        CheckActionExecutor(),
    )

    registry.register(
        "keyboard",
        KeyboardActionExecutor(),
    )

    registry.register(
        "file",
        FileActionExecutor(),
    )

    registry.register(
        "wait",
        WaitActionExecutor(),
    )

    registry.register(
        "evaluate",
        EvaluateActionExecutor(),
    )

    return registry
def create_state_detector_registry(
    resolver: ProviderResolver[Any, Any],
) -> BrowserPageStateDetectorRegistry:

    registry = BrowserPageStateDetectorRegistry()

    registry.register(
        "cloudflare",
        CloudflareChallengeDetector(),
    )

    registry.register(
        "turnstile",
        TurnstileChallengeDetector(),
    )

    registry.register(
        "captcha",
        CaptchaDetector(),
    )

    registry.register(
        "login",
        LoginRequiredDetector(),
    )

    registry.register(
        "access_denied",
        AccessDeniedDetector(),
    )

    registry.register(
        "normal",
        NormalPageDetector(),
    )

    return registry