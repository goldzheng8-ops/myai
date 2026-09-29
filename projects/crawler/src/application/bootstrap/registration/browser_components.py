from typing import Any
from core.request.browser.detector.captcha import CaptchaDetector
from core.request.browser.detector.access_denied import AccessDeniedDetector
from core.request.browser.detector.cloudflare_challenge import CloudflareChallengeDetector
from core.request.browser.detector.human_verification import HumanVerificationChallengeDetector
from core.request.browser.detector.login_required import LoginRequiredDetector
# from core.request.browser.detector.normal import NormalPageDetector
from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.detector.turnstile_challenge import TurnstileChallengeDetector
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.inspector.playwright import PlaywrightBrowserPageInspector
from core.request.browser.interaction.base import BrowserInteractionEngine
from core.request.browser.interaction.playwright import PlaywrightBrowserInteractionEngine
from core.request.browser.executor.registry import BrowserActionExecutorRegistry
from core.request.browser.executor.navigation import NavigationActionExecutor
from core.request.browser.executor.locator import LocatorActionExecutor
from core.request.browser.executor.input import InputActionExecutor
from core.request.browser.executor.selection import SelectionActionExecutor
from core.request.browser.executor.check import CheckActionExecutor
from core.request.browser.executor.keyboard import KeyboardActionExecutor
from core.request.browser.executor.file import FileActionExecutor
from core.request.browser.executor.wait import WaitActionExecutor
from core.request.browser.executor.evaluate import EvaluateActionExecutor
from application.config.model import ApplicationConfig
from core.provider import ProviderBuilder, ProviderResolver
from core.request.browser.intervention.factory import build_manual_console_intervention_factory
from core.request.browser.intervention.handler.Console import ConsoleHumanInterventionHandler
from core.request.browser.intervention.registry import HumanInterventionEngineRegistry
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.request.browser.snapshot import BrowserPageSnapshotBuilder, PlaywrightBrowserPageSnapshotBuilder
from core.request.downloader.extractor.playwright import PlaywrightCookieExtractor
from core.request.browser.typing import BrowserPageState

def register_browser_components(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    builder.add_type(ConsoleHumanInterventionHandler)
    builder.add_factory(
        BrowserRuntimeManager,
        lambda resolver: BrowserRuntimeManager(
            config=config.browser_runtime,
            context_config=config.browser_context,
            cookie_extractor=resolver.resolve(PlaywrightCookieExtractor)

        ),
    )
    builder.add_factory(
        BrowserPageSnapshotBuilder,
        lambda resolver: PlaywrightBrowserPageSnapshotBuilder(
            config=config.page_snapshot
        ),
    )
    builder.add_factory(
        BrowserPageInspector,
        lambda resolver: PlaywrightBrowserPageInspector(
            detector_registry=resolver.resolve(
                BrowserPageStateDetectorRegistry,
            ),
            snapshot_builder=resolver.resolve(
                BrowserPageSnapshotBuilder,
            ),
        ),
    )
    builder.add_factory(
        BrowserInteractionEngine,
        lambda resolver: PlaywrightBrowserInteractionEngine(
            inspector=resolver.resolve(
                BrowserPageInspector,
            ),
            human_intervention_registry=resolver.resolve(
                HumanInterventionEngineRegistry,
            ),
            executor_registry=resolver.resolve(
                BrowserActionExecutorRegistry,
            ),
        ),
    )
    builder.add_factory(
        BrowserActionExecutorRegistry,
        lambda resolver: create_action_executor_registry(
            resolver,
        ),
    )
    builder.add_factory(
        BrowserPageStateDetectorRegistry,
        lambda resolver: create_state_detector_registry(
            resolver,
        ),
    )
    builder.add_factory(
        HumanInterventionEngineRegistry,
        lambda resolver: create_human_intervention_registry(
            resolver=resolver,
            config=config,
        ),
    )

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
def create_human_intervention_registry(
    *,
    resolver: ProviderResolver[Any, Any],
    config: ApplicationConfig,
) -> HumanInterventionEngineRegistry:

    registry = HumanInterventionEngineRegistry()

    registry.register(
        BrowserPageState.CHALLENGE,
        build_manual_console_intervention_factory(
            resolver=resolver,
            config=config,
        ),
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
        "human_verification",
        HumanVerificationChallengeDetector(),
    )

    registry.register(
        "login",
        LoginRequiredDetector(),
    )

    registry.register(
        "access_denied",
        AccessDeniedDetector(),
    )

    # registry.register(
    #     "normal",
    #     NormalPageDetector(),
    # )

    return registry