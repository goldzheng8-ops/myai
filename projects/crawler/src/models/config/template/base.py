from abc import ABC

from models.config.base import BaseConfig

class TemplateConfig(
    BaseConfig,
    ABC,
):
    """Base configuration for template renderers."""

