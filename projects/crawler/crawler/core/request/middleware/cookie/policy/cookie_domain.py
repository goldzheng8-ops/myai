from __future__ import annotations
from ipaddress import ip_address

from core.request.middleware.cookie.policy.exception import InvalidCookieDomain
from core.request.middleware.cookie.policy.model import CookieDomainResolution
from core.request.middleware.cookie.policy.protocol import PublicSuffixMatcher


class CookieDomainPolicy:

    def __init__(
        self,
        public_suffix_matcher: PublicSuffixMatcher,
    ) -> None:
        self._public_suffix_matcher = public_suffix_matcher

    def resolve_set_cookie_domain(
        self,
        *,
        request_host: str,
        domain_attribute: str | None,
    ) -> CookieDomainResolution:
        """
        Resolve the Domain attribute of a raw Set-Cookie header.

        domain_attribute=None means that the Domain attribute
        was not present and therefore produces a host-only cookie.
        """

        host = self._normalize_host(request_host)

        if domain_attribute is None:
            return CookieDomainResolution(
                scope_domain=host,
                host_only=True,
            )

        domain = self._normalize_domain(
            domain_attribute,
        )

        # The Domain attribute is present but invalid.
        if domain is None:
            raise InvalidCookieDomain(
                f"Invalid cookie domain: {domain_attribute!r}",
            )

        return self._resolve_explicit_domain(
            host=host,
            domain=domain,
        )

    def resolve_parsed_domain(
        self,
        *,
        request_host: str,
        domain: str,
        host_only: bool,
    ) -> CookieDomainResolution:
        """
        Resolve the domain information of an already parsed
        stdlib http.cookiejar.Cookie.

        Unlike Set-Cookie parsing, the Domain attribute has already
        been interpreted by the transport library.

        Therefore:
        - host_only=True means the original cookie was host-only
        - host_only=False means the original cookie had a Domain attribute
        """

        host = self._normalize_host(request_host)

        normalized_domain = self._normalize_domain(
            domain,
        )

        if normalized_domain is None:
            raise InvalidCookieDomain(
                f"Invalid parsed cookie domain: {domain!r}",
            )

        if host_only:
            return CookieDomainResolution(
                scope_domain=host,
                host_only=True,
            )

        return self._resolve_explicit_domain(
            host=host,
            domain=normalized_domain,
        )

    def _resolve_explicit_domain(
        self,
        *,
        host: str,
        domain: str,
    ) -> CookieDomainResolution:

        if self._is_ip_address(host):
            if domain != host:
                raise InvalidCookieDomain(
                    f"Cookie domain {domain!r} "
                    f"does not match IP host {host!r}.",
                )

            return CookieDomainResolution(
                scope_domain=host,
                host_only=False,
            )

        if not self._domain_matches(
            host,
            domain,
        ):
            raise InvalidCookieDomain(
                f"Cookie domain {domain!r} "
                f"does not match host {host!r}.",
            )

        if self._public_suffix_matcher.is_public_suffix(
            domain,
        ):
            # A public suffix equal to the request host is treated
            # as host-only.
            if domain == host:
                return CookieDomainResolution(
                    scope_domain=host,
                    host_only=True,
                )

            raise InvalidCookieDomain(
                f"Cookie domain {domain!r} "
                "is a public suffix.",
            )

        return CookieDomainResolution(
            scope_domain=domain,
            host_only=False,
        )

    @staticmethod
    def _normalize_host(
        host: str,
    ) -> str:
        host = host.strip().rstrip(".")

        if not host:
            raise InvalidCookieDomain(
                "Cookie request host is empty.",
            )

        # IP addresses must not go through IDNA.
        if CookieDomainPolicy._is_ip_address(host):
            return host.lower()

        return CookieDomainPolicy._normalize_idna(
            host,
        )

    @staticmethod
    def _normalize_domain(
        domain: str,
    ) -> str | None:

        domain = domain.strip()

        if not domain:
            return None

        # Leading dot in Domain= is ignored.
        domain = domain.lstrip(".")

        # A trailing dot is not silently removed.
        # It represents an invalid Domain attribute.
        if domain.endswith("."):
            return None

        if not domain:
            return None

        if CookieDomainPolicy._is_ip_address(domain):
            return domain.lower()

        try:
            return CookieDomainPolicy._normalize_idna(
                domain,
            )
        except UnicodeError:
            return None

    @staticmethod
    def _normalize_idna(
        value: str,
    ) -> str:
        return (
            value
            .encode("idna")
            .decode("ascii")
            .lower()
        )

    @staticmethod
    def _is_ip_address(
        value: str,
    ) -> bool:
        try:
            ip_address(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def _domain_matches(
        host: str,
        domain: str,
    ) -> bool:
        if host == domain:
            return True

        return host.endswith(
            f".{domain}",
        )