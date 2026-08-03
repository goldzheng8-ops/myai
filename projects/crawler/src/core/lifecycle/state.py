from enum import Enum


class LifecycleState(str, Enum):
    """
    生命周期状态。
    """

    CREATED = "created"

    STARTING = "starting"

    RUNNING = "running"

    STOPPING = "stopping"

    STOPPED = "stopped"

    FAILED = "failed"