from dataclasses import dataclass

from core.request.discovery.engine import DiscoveryEngine
from core.extraction.extractor.engine import ExtractEngine
from core.extraction.response.factory import (
    ResponseAdapterFactory,
)
from core.request.runner import RequestRunner




@dataclass(frozen=True, slots=True)
class SpiderServices:
    """
    Framework services available to spider templates.
    """

    request_runner: RequestRunner

    extract_engine: ExtractEngine

    discovery_engine: DiscoveryEngine

    response_adapter_factory: ResponseAdapterFactory