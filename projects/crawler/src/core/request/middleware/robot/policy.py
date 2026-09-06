from abc import ABC, abstractmethod

class RobotsPolicy(ABC):

    @abstractmethod
    async def allowed(
        self,
        *,
        url: str,
        user_agent: str,
    ) -> bool:
        raise NotImplementedError
