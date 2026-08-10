from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthPolicy:

    enabled: bool = True

    override_headers: bool = False

    override_cookies: bool = False

    override_params: bool = False