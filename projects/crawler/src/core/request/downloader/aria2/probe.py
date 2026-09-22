from __future__ import annotations

import httpx


class Aria2RpcProbe:
    """
    Lightweight probe for an aria2 JSON-RPC endpoint.

    The probe is intentionally independent from the main
    Aria2Client lifecycle.
    """

    def __init__(
        self,
        *,
        rpc_url: str,
        rpc_secret: str | None = None,
        timeout: float = 1.0,
    ) -> None:

        if timeout <= 0:
            raise ValueError(
                "timeout must be greater than zero.",
            )

        self._rpc_url = rpc_url
        self._rpc_secret = rpc_secret
        self._client = httpx.AsyncClient(
            timeout=timeout,
        )

    async def is_available(self) -> bool:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "aria2.getVersion",
            "params": (
                [f"token:{self._rpc_secret}"]
                if self._rpc_secret is not None
                else []
            ),
        }

        try:
            response = await self._client.post(
                self._rpc_url,
                json=payload,
            )

            if not response.is_success:
                return False

            data = response.json()

            return (
                isinstance(data, dict)
                and "result" in data
                and "error" not in data
            )

        except (
            httpx.HTTPError,
            OSError,
            ValueError,
        ):
            return False

    async def close(self) -> None:
        await self._client.aclose()