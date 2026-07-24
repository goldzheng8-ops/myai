from config.discovery.base import ApiDiscoveryConfig


class OffsetApiConfig(ApiDiscoveryConfig):

    parameter: str = "offset"

    limit: int = 20

    start: int = 0

