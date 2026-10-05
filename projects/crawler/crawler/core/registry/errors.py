from __future__ import annotations


class RegistryError(Exception):
    """
    Base registry exception.
    """


class RegistryFrozenError(RegistryError):
    """
    Registry has been frozen.
    """


class RegistryKeyError(RegistryError):
    """
    Registry key not found.
    """


class RegistryExistsError(RegistryError):
    """
    Registry key already exists.
    """