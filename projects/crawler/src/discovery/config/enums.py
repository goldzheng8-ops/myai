from enum import Enum


class DiscoveryType(str, Enum):
    NEXT_PAGE = "next_page"
    PAGE_NUMBER = "page_number"
    DETAIL_LINK = "detail_link"
    API_CURSOR = "api_cursor"
    INFINITE_SCROLL = "infinite_scroll"