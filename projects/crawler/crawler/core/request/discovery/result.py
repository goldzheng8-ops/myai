from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.request.descriptor import RequestDescriptor

from .typing import DiscoveryType


@dataclass(frozen=True, slots=True)
class DiscoveryMetadata:
    """
    Metadata describing how a request was discovered.
    """

    source_url: str | None = None

    source_fingerprint: str | None = None

    discovery_type: DiscoveryType | None = None

    position: int | None = None

    depth: int = 0

    extras: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class DiscoveryRecord:
    """
    A request discovered from a response.
    """

    descriptor: RequestDescriptor

    metadata: DiscoveryMetadata = field(
        default_factory=DiscoveryMetadata,
    )


@dataclass(slots=True)
class DiscoveryResult:
    """
    Result produced by discovery execution.
    """

    records: list[DiscoveryRecord] = field(
        default_factory=list,
    )