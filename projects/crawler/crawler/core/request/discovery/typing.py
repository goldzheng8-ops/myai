from enum import Enum


class DiscoveryType(str,Enum):

    PAGINATION = "pagination"

    HTML = "html"

    RSS = "rss"

    SITEMAP = "sitemap"

    FILE = "file"

    CURSOR_API = "cursor_api"

    INFINITE_SCROLL = "infinite_scroll"

    OFFSET_API="offset_api"

    GRAPHQL_CURSOR = "graphql_cursor"

