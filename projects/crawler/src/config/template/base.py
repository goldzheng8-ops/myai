from abc import ABC

from core.models.base import BaseConfig

class TemplateConfig(
    BaseConfig,
    ABC,
):
    """Base configuration for template renderers."""

