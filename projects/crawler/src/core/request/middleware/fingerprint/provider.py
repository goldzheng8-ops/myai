from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any, Protocol, cast

from core.request.descriptor import RequestDescriptor


class FingerprintProvider(Protocol):
    """
    Provides a deterministic fingerprint for a request descriptor.
    """

    def fingerprint(
        self,
        descriptor: RequestDescriptor,
    ) -> str:
        ...


class DefaultFingerprintProvider:
    """
    Default SHA-256 based request fingerprint provider.

    The fingerprint is derived from:

    - HTTP method
    - normalized URL
    - normalized query parameters
    - normalized request body

    Headers, cookies, proxy settings, timeout and other
    execution-related properties are intentionally excluded.
    """

    def fingerprint(
        self,
        descriptor: RequestDescriptor,
    ) -> str:

        canonical = self._canonicalize(
            descriptor,
        )

        return hashlib.sha256(
            canonical.encode("utf-8"),
        ).hexdigest()

    def _canonicalize(
        self,
        descriptor: RequestDescriptor,
    ) -> str:

        payload = {
            "method": str(descriptor.method),
            "url": self._normalize_url(
                descriptor.url,
            ),
            "params": self._normalize_value(
                descriptor.params,
            ),
            "body": self._normalize_value(
                descriptor.body,
            ),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _normalize_url(
        url: str,
    ) -> str:

        return url.strip()

    def _normalize_value(
        self,
        value: Any,
    ) -> Any:

        if value is None:
            return None

        if isinstance(value, Mapping):

            mapping_value = cast(Mapping[Any, Any], value)

            return {
                str(key): self._normalize_value(item)
                for key, item in sorted(
                    mapping_value.items(),
                    key=lambda item: str(item[0]),
                )
            }

        if isinstance(value, Sequence) and not isinstance(
            value,
            (str, bytes, bytearray),
        ):

            sequence_value = cast(Sequence[Any], value)

            return [
                self._normalize_value(item)
                for item in sequence_value
            ]

        if isinstance(value, bytes):

            return value.hex()

        return value