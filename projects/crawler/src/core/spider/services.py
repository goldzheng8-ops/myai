from dataclasses import dataclass

from core.input.engine import InputEngine
from core.output.engine import OutputEngine
from core.request.discovery.engine import DiscoveryEngine
from core.extraction.extractor.executor import ExtractExecutor
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.runner import RequestRunner
from core.request.browser.interaction.base import BrowserInteractionEngine



@dataclass(frozen=True, slots=True)
class SpiderServices:
    """
    Framework services available to spider templates.
    """

    request_runner: RequestRunner

    extract_executor: ExtractExecutor

    discovery_engine: DiscoveryEngine

    fingerprint_provider: FingerprintProvider

    output_engine:OutputEngine

    input_engine: InputEngine

    browser_interaction_engine: BrowserInteractionEngine