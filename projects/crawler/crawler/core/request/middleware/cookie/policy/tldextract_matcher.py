from __future__ import annotations
import tldextract


class TldExtractPublicSuffixMatcher:
    def __init__(
        self,
        *,
        include_private_domains: bool = True,
    ) -> None:
        self._extractor = tldextract.TLDExtract(
            include_psl_private_domains=include_private_domains,
            suffix_list_urls=(),
        )

    def is_public_suffix(
        self,
        domain: str,
    ) -> bool:
        domain = domain.strip().lower()

        if not domain:
            return False

        result = self._extractor(domain)

        return bool(result.suffix) and not bool(result.domain)