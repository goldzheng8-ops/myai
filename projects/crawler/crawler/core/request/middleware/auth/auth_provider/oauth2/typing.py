
from enum import Enum


class OAuth2TokenState(str,Enum):
    ACTIVE = "active"
    INVALID = "invalid"