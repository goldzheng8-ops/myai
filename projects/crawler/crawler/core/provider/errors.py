class ProviderError(RuntimeError):
    """Base provider exception."""


class ProviderFrozenError(ProviderError):
    """Registry is frozen."""


class ServiceNotRegisteredError(ProviderError):
    """Service not registered."""