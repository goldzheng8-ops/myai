from typing import Any
import httpx
import asyncio
from .exception import (
    Aria2RpcError,
    Aria2RpcErrorInfo,
)
from .model import (
    Aria2DownloadStatus,
    Aria2File,
    Aria2Status,
    is_json_object,
)




class Aria2Client:

    def __init__(
        self,
        *,
        rpc_url: str,
        rpc_secret: str | None = None,
        timeout: float | None = 30.0,
    ) -> None:

        self._rpc_url = rpc_url
        self._rpc_secret = rpc_secret
        self._timeout = timeout

        self._client: httpx.AsyncClient | None = None

        self._request_id = 0

        self._request_id_lock = (
            asyncio.Lock()
        )

    async def start(self) -> None:

        if self._client is not None:
            return

        self._client = httpx.AsyncClient(
            timeout=self._timeout,
        )

    async def close(self) -> None:

        client = self._client

        if client is None:
            return

        self._client = None

        await client.aclose()

    async def add_uri(
        self,
        *,
        uri: str,
        options: dict[str, Any] | None = None,
    ) -> str:

        params: list[Any] = []

        if self._rpc_secret is not None:
            params.append(
                f"token:{self._rpc_secret}",
            )

        params.append([uri])

        if options:
            params.append(options)

        result = await self._call(
            method="aria2.addUri",
            params=params,
        )

        if not isinstance(result, str):
            raise RuntimeError(
                "aria2.addUri returned an invalid "
                "GID.",
            )

        return result

    async def tell_status(
        self,
        gid: str,
    ) -> Aria2DownloadStatus:

        params: list[Any] = []

        if self._rpc_secret is not None:
            params.append(
                f"token:{self._rpc_secret}",
            )

        params.append(gid)

        result = await self._call(
            method="aria2.tellStatus",
            params=params,
        )

        if not is_json_object(result):
            raise RuntimeError(
                "aria2.tellStatus returned an invalid "
                "response.",
            )

        return self._parse_status(result)

    async def force_remove(
        self,
        gid: str,
    ) -> None:

        params: list[Any] = []

        if self._rpc_secret is not None:
            params.append(
                f"token:{self._rpc_secret}",
            )

        params.append(gid)

        await self._call(
            method="aria2.forceRemove",
            params=params,
        )

    async def pause(
        self,
        gid: str,
    ) -> None:

        params: list[Any] = []

        if self._rpc_secret is not None:
            params.append(
                f"token:{self._rpc_secret}",
            )

        params.append(gid)

        await self._call(
            method="aria2.pause",
            params=params,
        )

    async def unpause(
        self,
        gid: str,
    ) -> None:

        params: list[Any] = []

        if self._rpc_secret is not None:
            params.append(
                f"token:{self._rpc_secret}",
            )

        params.append(gid)

        await self._call(
            method="aria2.unpause",
            params=params,
        )

    async def _call(
        self,
        *,
        method: str,
        params: list[Any],
    ) -> Any:

        client = self._require_client()

        request_id = (
            await self._next_request_id()
        )

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        response = await client.post(
            self._rpc_url,
            json=payload,
        )

        response.raise_for_status()

        data: Any = response.json()

        if not is_json_object(data):
            raise RuntimeError(
                "Invalid aria2 JSON-RPC response.",
            )

        error = data.get("error")

        if error is not None:

            if not is_json_object(error):
                raise RuntimeError(
                    "Invalid aria2 JSON-RPC error.",
                )

            raise self._build_rpc_error(
                error,
            )

        if "result" not in data:
            raise RuntimeError(
                "aria2 JSON-RPC response does not "
                "contain a result.",
            )

        return data["result"]

    
    async def _next_request_id(
        self,
    ) -> int:

        async with self._request_id_lock:

            self._request_id += 1

            return self._request_id

    def _require_client(
        self,
    ) -> httpx.AsyncClient:

        client = self._client

        if client is None:
            raise RuntimeError(
                "Aria2Client is not started.",
            )

        return client

    @staticmethod
    def _parse_status(
        data: dict[str, Any],
    ) -> Aria2DownloadStatus:

        gid = Aria2Client._require_string(
            data,
            "gid",
        )

        status_text = Aria2Client._require_string(
            data,
            "status",
        )

        try:
            status = Aria2Status(
                status_text,
            )
        except ValueError as exc:
            raise RuntimeError(
                f"Unknown aria2 status: "
                f"{status_text!r}",
            ) from exc

        files = Aria2Client._parse_files(
            data.get("files"),
        )

        return Aria2DownloadStatus(
            gid=gid,
            status=status,
            total_length=Aria2Client._parse_int(
                data,
                "totalLength",
            ),
            completed_length=Aria2Client._parse_int(
                data,
                "completedLength",
            ),
            download_speed=Aria2Client._parse_int(
                data,
                "downloadSpeed",
            ),
            upload_speed=Aria2Client._parse_int(
                data,
                "uploadSpeed",
            ),
            connections=Aria2Client._parse_int(
                data,
                "connections",
            ),
            error_code=Aria2Client._optional_string(
                data,
                "errorCode",
            ),
            error_message=Aria2Client._optional_string(
                data,
                "errorMessage",
            ),
            dir=Aria2Client._optional_string(
                data,
                "dir",
            ),
            files=files,
        )

    @staticmethod
    def _parse_files(
        value: Any,
    ) -> tuple[Aria2File, ...]:

        if value is None:
            return ()

        if not isinstance(value, list):
            raise RuntimeError(
                "Invalid aria2 files response.",
            )

        result: list[Aria2File] = []

        for item in value:

            if not is_json_object(item):
                raise RuntimeError(
                    "Invalid aria2 file entry.",
                )

            result.append(
                Aria2File(
                    path=Aria2Client._require_string(
                        item,
                        "path",
                    ),
                    length=Aria2Client._parse_int(
                        item,
                        "length",
                    ),
                    completed_length=(
                        Aria2Client._parse_int(
                            item,
                            "completedLength",
                        )
                    ),
                    selected=(
                        Aria2Client._require_string(
                            item,
                            "selected",
                        )
                        == "true"
                    ),
                ),
            )

        return tuple(result)

    @staticmethod
    def _require_string(
        data: dict[str, Any],
        key: str,
    ) -> str:

        value = data.get(key)

        if not isinstance(value, str):
            raise RuntimeError(
                f"aria2 field {key!r} "
                "must be a string.",
            )

        return value

    @staticmethod
    def _optional_string(
        data: dict[str, Any],
        key: str,
    ) -> str | None:

        value = data.get(key)

        if value is None:
            return None

        if not isinstance(value, str):
            raise RuntimeError(
                f"aria2 field {key!r} "
                "must be a string or null.",
            )

        return value

    @staticmethod
    def _parse_int(
        data: dict[str, Any],
        key: str,
    ) -> int:

        value = data.get(key)

        if not isinstance(value, str):
            raise RuntimeError(
                f"aria2 field {key!r} "
                "must be a string.",
            )

        try:
            return int(value)

        except ValueError as exc:
            raise RuntimeError(
                f"Invalid integer value for "
                f"aria2 field {key!r}: {value!r}",
            ) from exc

    @staticmethod
    def _build_rpc_error(
        data: dict[str, Any],
    ) -> Aria2RpcError:

        code = data.get("code")
        message = data.get("message")
        error_data = data.get("data")

        if not isinstance(code, int):
            raise RuntimeError(
                "Invalid aria2 RPC error code.",
            )

        if not isinstance(message, str):
            raise RuntimeError(
                "Invalid aria2 RPC error message.",
            )

        return Aria2RpcError(
            Aria2RpcErrorInfo(
                code=code,
                message=message,
                data=error_data,
            ),
        )