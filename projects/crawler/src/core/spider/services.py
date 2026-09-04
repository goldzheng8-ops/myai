from dataclasses import dataclass

from core.request.discovery.engine import DiscoveryEngine
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.response.resolver import (
    ResponseAdapterResolver,
)
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.runner import RequestRunner




@dataclass(frozen=True, slots=True)
class SpiderServices:
    """
    Framework services available to spider templates.
    """

    request_runner: RequestRunner

    extract_engine: ExtractExecutor

    discovery_engine: DiscoveryEngine

    fingerprint_provider: FingerprintProvider

    response_adapter_resolver: ResponseAdapterResolver