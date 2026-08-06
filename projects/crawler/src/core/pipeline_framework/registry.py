from __future__ import annotations

from core.event.registry import MultiRegistry

from .pipeline import Pipeline
from .typing import ContextT

class PipelineRegistry(
    MultiRegistry[str, Pipeline[ContextT]]
):
    pass