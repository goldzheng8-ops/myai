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

        self._public_suffix_matcher = (
            public_suffix_matcher
        )

    def resolve(
        self,
        *,
        request_host: str,
        domain_attribute: str | None,
    ) -> CookieDomainResolution:

        host = self._normalize_host(
            request_host,
        )

        # -----------------------------------------------------
        # No Domain attribute
        #
        # Host-only cookie.
        # -----------------------------------------------------

        if domain_attribute is None:

            return CookieDomainResolution(
                scope_domain=host,
                host_only=True,
            )

        # -----------------------------------------------------
        # Domain attribute
        # -----------------------------------------------------

        domain = self._normalize_domain(
            domain_attribute,
        )

        if domain is None:
            raise InvalidCookieDomain(
                "Invalid Cookie Domain attribute.",
            )

        # -----------------------------------------------------
        # IP address
        # -----------------------------------------------------

        if self._is_ip_address(host):

            if domain != host:
                raise InvalidCookieDomain(
                    "Cookie Domain does not match "
                    f"request host: {domain!r} "
                    f"!= {host!r}",
                )

            return CookieDomainResolution(
                scope_domain=host,
                host_only=False,
            )

        # -----------------------------------------------------
        # Domain must include request host.
        # -----------------------------------------------------

        if not self._domain_matches(
            host,
            domain,
        ):
            raise InvalidCookieDomain(
                "Cookie Domain does not match "
                f"request host: {domain!r} / {host!r}",
            )

        # -----------------------------------------------------
        # Public suffix.
        #
        # If the Domain itself equals the request host,
        # RFC 6265 permits treating it as host-only.
        #
        # Otherwise reject it.
        # -----------------------------------------------------

        if self._public_suffix_matcher.is_public_suffix(
            domain,
        ):

            if domain == host:

                return CookieDomainResolution(
                    scope_domain=host,
                    host_only=True,
                )

            raise InvalidCookieDomain(
                "Cookie Domain is a public suffix: "
                f"{domain!r}",
            )

        return CookieDomainResolution(
            scope_domain=domain,
            host_only=False,
        )

    # ---------------------------------------------------------
    # normalization
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_host(
        host: str,
    ) -> str:

        host = host.strip().lower()

        if not host:
            raise InvalidCookieDomain(
                "Request host is empty.",
            )

        if host.endswith("."):
            host = host[:-1]

        if not host:
            raise InvalidCookieDomain(
                "Request host is invalid.",
            )

        return host

    @staticmethod
    def _normalize_domain(
        value: str,
    ) -> str | None:

        domain = value.strip().lower()

        if not domain:
            return None

        # RFC 6265:
        #
        # A leading dot is ignored.
        if domain.startswith("."):
            domain = domain[1:]

        if not domain:
            return None

        # IMPORTANT:
        #
        # A trailing dot causes the Domain attribute
        # to be ignored. It must NOT be silently removed.
        if domain.endswith("."):
            return None

        return domain

    # ---------------------------------------------------------
    # domain matching
    # ---------------------------------------------------------

    @staticmethod
    def _domain_matches(
        host: str,
        domain: str,
    ) -> bool:

        if host == domain:
            return True

        if CookieDomainPolicy._is_ip_address(
            host,
        ):
            return False

        if not host.endswith(domain):
            return False

        boundary = (
            len(host)
            - len(domain)
            - 1
        )

        return (
            boundary >= 0
            and host[boundary] == "."
        )

    # ---------------------------------------------------------
    # IP
    # ---------------------------------------------------------

    @staticmethod
    def _is_ip_address(
        value: str,
    ) -> bool:

        try:
            ip_address(value)
        except ValueError:
            return False

        return True