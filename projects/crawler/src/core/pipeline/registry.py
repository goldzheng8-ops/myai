from typing import Generic

from core.registry.base import Registry

from .pipeline import Pipeline
from .typing import ContextT


class PipelineRegistry(
    Registry[
        str,
        Pipeline[ContextT],
    ],
    Generic[ContextT],
):
    """
    Registry of pipelines.
    """