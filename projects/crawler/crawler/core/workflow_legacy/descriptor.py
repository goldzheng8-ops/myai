# core/workflow/descriptor.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True,kw_only=True)
class WorkflowDescriptor:
    """
    Base descriptor for workflow definitions.
    """

    name: str

    description: str = ""

    enabled: bool = True