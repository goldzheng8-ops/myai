from bs4 import Tag
from bs4 import BeautifulSoup

from adapters.base import ResponseAdapter



class BeautifulSoupAdapter(ResponseAdapter):
    def __init__(self, soup: BeautifulSoup | Tag):
        self._soup = soup

