from core.extraction.extractor.engine import ExtractEngine
from core.extraction.response.factory import ResponseAdapterFactory
from core.provider import ProviderBuilder
from core.request.discovery.engine import DiscoveryEngine
from core.request.middleware.fingerprint import FingerprintProvider
from core.request.runner import RequestRunner
from core.spider.services import SpiderServices


def register_spider_services(
        builder: ProviderBuilder,
    ) -> None:

        builder.add_factory(
            SpiderServices,
            lambda resolver: SpiderServices(
                request_runner=resolver.resolve(RequestRunner),
                extract_engine=resolver.resolve(ExtractEngine),
                discovery_engine=resolver.resolve(DiscoveryEngine),
                fingerprint_provider=resolver.resolve(FingerprintProvider),
                response_adapter_factory=resolver.resolve(ResponseAdapterFactory),
            ),
        )