from __future__ import annotations

from typing import TypeVar

from .context import PipelineContext

ContextT = TypeVar("ContextT", bound=PipelineContext)
