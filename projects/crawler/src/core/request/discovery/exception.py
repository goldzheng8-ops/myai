from core.exception.application import CrawlerError


class DiscoveryError(CrawlerError):
    """Base exception for URL discovery failures."""