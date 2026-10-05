class EventError(RuntimeError):
    """Base exception for event infrastructure failures."""


class EventDispatchError(EventError):
    """Raised when an event cannot be dispatched."""


class EventHandlerError(EventError):
    """Raised when a handler fails to execute."""