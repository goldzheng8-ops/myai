from typing import Any

from core.extraction.transform.factory import TransformFactory
from core.extraction.transform.typing import TransformType
from core.extraction.transform.base import TransformPlugin
from core.registry.base import Registry



class TransformRegistry(
    Registry[
        TransformType,
        TransformFactory,
    ],
):
    """
    Registry of transform plugin factories.
    """

    def create(
        self,
        type_: TransformType,
    ) -> TransformPlugin[Any, Any, Any]:

        return self.get(type_)()