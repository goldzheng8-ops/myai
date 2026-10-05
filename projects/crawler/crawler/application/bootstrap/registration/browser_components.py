from typing import Any
from core.request.browser.detector.captcha import CaptchaDetector
from core.request.browser.detector.access_denied import AccessDeniedDetector
from core.request.browser.detector.cloudflare_challenge import CloudflareChallengeDetector
from core.request.browser.detector.human_verification import HumanVerificationChallengeDetector
from core.request.browser.detector.login_required import LoginRequiredDetector
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
from core.provider.protocol import ProviderResolver
from core.provider.builder import ProviderBuilder
from core.request.browser.intervention.factory import build_manual_console_intervention_factory
from core.request.browser.intervention.handler.Console import ConsoleHumanInterventionHandler
from core.request.browser.intervention.registry import HumanInterventionEngineRegistry

from core.request.browser.runtime_manager import BrowserRuntimeDebugger, BrowserRuntimeManager
from core.request.browser.snapshot import BrowserPageSnapshotBuilder, PlaywrightBrowserPageSnapshotBuilder
from core.request.browser.stabilizer.playwright import PlaywrightBrowserPageStabilizer
from core.request.browser.stabilizer.base import BrowserPageStabilizer
from core.request.browser.stabilizer.policy.challenge import ChallengeStabilityPolicy
from core.request.browser.stabilizer.policy.interaction import InteractionStabilityPolicy
from core.request.browser.stabilizer.policy.registry import BrowserPageStabilityPolicyRegistry
from core.request.browser.stabilizer.policy.strict import StrictStabilityPolicy
from core.request.downloader.extractor.playwright import PlaywrightCookieExtractor
from core.request.browser.typing import BrowserPageState, BrowserInteractionPhase
from core.request.middleware.auth.auth_provider.oauth2.refresher import OAuth2TokenRefresher
from core.runtime.parser import ResolveExpressionParser

def register_browser_components(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_type(
        ResolveExpressionParser,
    )
    builder.add_type(
        NavigationActionExecutor,
    )

    builder.add_type(
        LocatorActionExecutor,
    )

    builder.add_type(
        InputActionExecutor,
    )

    builder.add_type(
        SelectionActionExecutor,
    )

    builder.add_type(
        CheckActionExecutor,
    )

    builder.add_type(
        KeyboardActionExecutor,
    )

    builder.add_type(
        FileActionExecutor,
    )

    builder.add_type(
        WaitActionExecutor,
    )

    builder.add_type(
        EvaluateActionExecutor,
    )

    builder.add_type(ConsoleHumanInterventionHandler)

    builder.add_factory(
        BrowserRuntimeManager,
        lambda resolver: BrowserRuntimeManager(
            config=config.browser_runtime,
            context_config=config.browser_context,
            cookie_extractor=resolver.resolve(PlaywrightCookieExtractor),
            debugger=resolver.resolve(BrowserRuntimeDebugger),
            oauth2_token_refresher=resolver.resolve(OAuth2TokenRefresher),

        ),
    )
    builder.add_factory(
        BrowserPageSnapshotBuilder,
        lambda resolver: PlaywrightBrowserPageSnapshotBuilder(
            config=config.page_snapshot
        ),
    )
    builder.add_factory(
        BrowserRuntimeDebugger,
        lambda resolver: BrowserRuntimeDebugger(
            config=config.browser_runtime
        ),
    )
    builder.add_factory(
        BrowserPageInspector,
        lambda resolver: PlaywrightBrowserPageInspector(
            detector_registry=resolver.resolve(
                BrowserPageStateDetectorRegistry,
            ),
            stabilizer=resolver.resolve(
                BrowserPageStabilizer,
            ),
            debugger=resolver.resolve(
                BrowserRuntimeDebugger,
            ),
        ),
    )
    builder.add_factory(
        BrowserPageStabilizer,
        lambda resolver: PlaywrightBrowserPageStabilizer(
            snapshot_builder=resolver.resolve(
                BrowserPageSnapshotBuilder,
            ),
            policy_registry=resolver.resolve(
                BrowserPageStabilityPolicyRegistry,
            ),
            debugger=resolver.resolve(
                BrowserRuntimeDebugger,
            ),
        ),
    )
    builder.add_factory(
        BrowserInteractionEngine,
        lambda resolver: PlaywrightBrowserInteractionEngine(
            inspector=resolver.resolve(
                BrowserPageInspector,
            ),
            stabilizer=resolver.resolve(
                BrowserPageStabilizer,
            ),
            human_intervention_registry=resolver.resolve(
                HumanInterventionEngineRegistry,
            ),
            executor_registry=resolver.resolve(
                BrowserActionExecutorRegistry,
            ),
            debugger=resolver.resolve(
                BrowserRuntimeDebugger,
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
        BrowserPageStabilityPolicyRegistry,
        lambda resolver: create_stability_policy_registry(
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
        resolver.resolve(
            NavigationActionExecutor,
        ),
    )

    registry.register(
        "locator",
        resolver.resolve(
            LocatorActionExecutor,
        ),
    )

    registry.register(
        "input",
        resolver.resolve(
            InputActionExecutor,
        ),
    )

    registry.register(
        "selection",
        resolver.resolve(
            SelectionActionExecutor,
        ),
    )

    registry.register(
        "check",
        resolver.resolve(
            CheckActionExecutor,
        ),
    )

    registry.register(
        "keyboard",
        resolver.resolve(
            KeyboardActionExecutor,
        ),
    )

    registry.register(
        "file",
        resolver.resolve(
            FileActionExecutor,
        ),
    )

    registry.register(
        "wait",
        resolver.resolve(
            WaitActionExecutor,
        ),
    )

    registry.register(
        "evaluate",
        resolver.resolve(
            EvaluateActionExecutor,
        ),
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
    registry.register(
        BrowserPageState.LOGIN_REQUIRED,
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


    return registry

def create_stability_policy_registry(
    resolver: ProviderResolver[Any, Any],
) -> BrowserPageStabilityPolicyRegistry:

    registry = BrowserPageStabilityPolicyRegistry()

    registry.register(
        BrowserInteractionPhase.INITIALIZING,
        StrictStabilityPolicy(),
    )
    registry.register(
        BrowserInteractionPhase.INTERACTING,
        InteractionStabilityPolicy(),
    )
    registry.register(
        BrowserInteractionPhase.HUMAN_INTERVENTION,
        ChallengeStabilityPolicy(),
    )
    registry.register(
        BrowserInteractionPhase.RECOVERY,
        ChallengeStabilityPolicy(),
    )
    registry.register(
        BrowserInteractionPhase.COMPLETED,
        StrictStabilityPolicy(),
    )


    return registry