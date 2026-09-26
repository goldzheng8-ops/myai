from typing import Protocol, Any
from core.request.middleware.cookie.model import Cookie

class CookieConverter(Protocol):
    @staticmethod
    def convert(cookie: Any) -> Cookie:
        ...