from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CookiePolicy:

    enabled: bool = True

    merge_session_cookies: bool = True

    update_session_cookies: bool = True