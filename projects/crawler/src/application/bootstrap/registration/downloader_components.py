from core.provider import ProviderBuilder
from core.request.middleware.cookie.policy.cookie_domain import CookieDomainPolicy
from core.request.middleware.cookie.policy.parser import SetCookieParser
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
    builder.add_instance(SetCookieParser,set_cookie_parser)
