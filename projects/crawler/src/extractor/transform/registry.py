from typing import Any

from enums.transform_type import TransformType
from extractor.transform.base import TransformPlugin
from core.registry.single import SingletonPluginRegistry




class TransformRegistry(
    SingletonPluginRegistry[
        TransformType,
        TransformPlugin[Any,Any],
    ],
):
    pass