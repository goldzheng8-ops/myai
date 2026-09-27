from core.provider import ProviderBuilder
from core.request.downloader.extractor.httpx import HttpxCookieExtractor
from core.request.downloader.extractor.playwright import PlaywrightCookieExtractor
from core.request.downloader.extractor.scrapy import ScrapyCookieExtractor
from core.request.middleware.cookie.cookie_converter import HttpCookieConverter
from core.request.middleware.cookie.policy.cookie_domain import CookieDomainPolicy
from core.request.middleware.cookie.cookie_parser import SetCookieParser
from core.request.middleware.cookie.policy.tldextract_matcher import TldExtractPublicSuffixMatcher


def register_downloader_components(
    builder: ProviderBuilder,
) -> None:

    public_suffix_matcher = (
        TldExtractPublicSuffixMatcher(
            include_private_domains=True,
        )
    )

    cookie_domain_policy = CookieDomainPolicy(
        public_suffix_matcher,
    )

    set_cookie_parser = SetCookieParser(
        cookie_domain_policy,
    )
    http_cookie_converter = HttpCookieConverter(
    cookie_domain_policy,
)
    builder.add_instance(SetCookieParser,set_cookie_parser)
    builder.add_instance(HttpCookieConverter,http_cookie_converter)
    builder.add_factory(
        ScrapyCookieExtractor,
        lambda resolver: ScrapyCookieExtractor(
            converter=resolver.resolve(
                HttpCookieConverter,
            ),
        ),
    )
    builder.add_factory(
        HttpxCookieExtractor,
        lambda resolver: HttpxCookieExtractor(
            converter=resolver.resolve(
                HttpCookieConverter,
            ),
        ),
    )
    builder.add_factory(
        PlaywrightCookieExtractor,
        lambda resolver: PlaywrightCookieExtractor(
            set_cookie_parser=resolver.resolve(
                SetCookieParser,
            ),
        ),
    )