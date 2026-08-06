from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, MutableMapping

#PipelineRuntime
@dataclass(slots=True)
class PipelineContext:
    """Base context object carried through a pipeline execution."""

    data: MutableMapping[str, Any] = field(default_factory=dict)
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    def get(
        self,
        key:str,
        default:str|None=None
    ):
        return self.data.get(
            key,
            default
        )


    def set(
        self,
        key:str,
        value:Any
    ):
        self.data[key]=value


    def copy(self) -> "PipelineContext":
        return type(self)(data=dict(self.data),metadata=dict(self.metadata),)
