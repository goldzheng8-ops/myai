from core.typing.config import BaseConfig

class RetryPolicyConfig(BaseConfig):
    retry_status_codes: frozenset[int] = frozenset({
        408,
        425,
        429,
        500,
        502,
        503,
        504,
    })