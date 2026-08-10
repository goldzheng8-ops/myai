from typing import Any

from models.enums.transform_type import TransformType
from core.extraction.transform.base import TransformPlugin
from core.registry.single import SingletonPluginRegistry




class TransformRegistry(
    SingletonPluginRegistry[
        TransformType,
        TransformPlugin[Any,Any],
    ],
):
    pass