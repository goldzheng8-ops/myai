from abc import ABC, abstractmethod


class Lifecycle(ABC):
    """
    所有需要管理生命周期的组件统一继承。
    """

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...

class LifecycleResolver(
    MultiResolver[
        type[Event],
        EventHandler,
    ],
):
    pass