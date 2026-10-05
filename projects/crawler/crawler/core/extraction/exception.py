# extraction/exception.py

from core.exception.application import ApplicationRuntimeError


class ExtractionError(ApplicationRuntimeError):
    """Base extraction error."""


class ValueResolutionError(ExtractionError):
    """Failed to resolve a value."""


class SelectorError(ValueResolutionError):
    """Selector execution failed."""


class TransformError(ExtractionError):
    """Transform execution failed."""


class RequiredFieldMissingError(ExtractionError):
    """Required field produced no value."""