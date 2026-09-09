# core/exception/application.py

from .base import ApplicationError


class ConfigurationError(ApplicationError):
    pass


class ApplicationRuntimeError(ApplicationError):
    pass