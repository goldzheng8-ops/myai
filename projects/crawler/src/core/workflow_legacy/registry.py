from __future__ import annotations

from core.registry.base import Registry

from .typing import ContextT
from .workflow import Workflow


class WorkflowRegistry(
    Registry[
        str,
        Workflow[ContextT],
    ],
):
    """
    Registry of named Workflow definitions.
    """

    pass