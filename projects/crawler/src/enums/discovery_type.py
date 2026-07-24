from enum import Enum


class DiscoveryType(str,Enum):

    DETAIL_LINK = "detail_link"

    NEXT_PAGE = "next_page"

    PAGE_NUMBER = "page_number"

    CURSOR_API = "cursor_api"

    INFINITE_SCROLL = "infinite_scroll"

    GRAPHQL_CURSOR = "graphql_cursor"
    OFFSET_API="offset_api"

    RSS = "rss"

    SITEMAP = "sitemap"