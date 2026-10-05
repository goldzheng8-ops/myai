from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Aria2RpcErrorInfo:
    code: int
    message: str
    data: object | None = None

class Aria2RpcError(
    RuntimeError,
):

    def __init__(
        self,
        error: Aria2RpcErrorInfo,
    ) -> None:

        self.error = error

        super().__init__(
            f"aria2 RPC error "
            f"{error.code}: {error.message}",
        )