from __future__ import annotations


class RetryError(Exception):
    """
    Base class for retry-related exceptions.
    """


class RetryableError(RetryError):
    """
    An exception that represents a transient failure
    and may be retried.
    """


class NonRetryableError(RetryError):
    """
    An exception that must not be retried.
    """