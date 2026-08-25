from .registry import DiscoveryRegistry
from .factory import (
    create_cursor_api_discovery,
    create_detail_link_discovery,
    create_infinite_scroll_discovery,
    create_next_page_discovery,
    create_offset_api_discovery,
    create_page_number_discovery,
    create_rss_discovery,
    create_sitemap_discovery,
)

__all__=[
    "DiscoveryRegistry",
    "create_cursor_api_discovery",
    "create_detail_link_discovery",
    "create_infinite_scroll_discovery",
    "create_next_page_discovery",
    "create_offset_api_discovery",
    "create_page_number_discovery",
    "create_rss_discovery",
    "create_sitemap_discovery",
]