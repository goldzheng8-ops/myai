from dataclasses import dataclass

from core.request.discovery.engine import DiscoveryEngine
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.response.factory import (
    ResponseAdapterFactory,
)
from core.request.middleware.fingerprint import FingerprintProvider
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

    response_adapter_factory: ResponseAdapterFactory