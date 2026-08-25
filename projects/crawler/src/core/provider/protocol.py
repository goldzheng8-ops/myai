from typing import  Generic, Protocol, Sequence

from core.typing.vars import T,K_contra,T_co

class ProviderResolver_(Protocol):

    def get(
        self,
        service: type[T],
    ) -> T:
        ...

class ProviderResolver(
    Protocol,
    Generic[K_contra, T_co],
):
    def resolve(
        self,
        key: K_contra,
    ) -> T_co:
        ...

class MultiResolver(
    Protocol,
    Generic[K_contra, T_co],
):

    def resolve(
        self,
        key: K_contra,
    ) -> Sequence[T_co]:
        ...

