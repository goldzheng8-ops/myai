from typing import Any

from core.extraction.transform.typing import TransformType
from core.extraction.transform.base import TransformPlugin
from core.registry.base import Registry




class TransformRegistry(
    Registry[
        TransformType,
        TransformPlugin[Any,Any,Any],
    ],
):
    pass