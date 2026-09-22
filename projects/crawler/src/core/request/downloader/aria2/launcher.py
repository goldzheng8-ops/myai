from __future__ import annotations

import asyncio
import os
import shutil

from core.request.downloader.aria2.probe import Aria2RpcProbe



class Aria2ProcessLauncher:
    """
    Manages the lifecycle of an aria2c RPC process.

    The launcher never terminates an aria2 process that it
    did not start itself.
    """

    def __init__(
        self,
        *,
        rpc_url: str,
        executable: str = "aria2c",
        rpc_port: int = 6800,
        rpc_secret: str | None = None,
        startup_timeout: float = 10.0,
        auto_start: bool = True,
    ) -> None:

        if startup_timeout <= 0:
            raise ValueError(
                "startup_timeout must be greater than zero.",
            )

        self._rpc_url = rpc_url
        self._executable = executable
        self._rpc_port = rpc_port
        self._rpc_secret = rpc_secret
        self._startup_timeout = startup_timeout
        self._auto_start = auto_start

        self._probe = Aria2RpcProbe(
            rpc_url=rpc_url,
            rpc_secret=rpc_secret,
        )

        self._process: (
            asyncio.subprocess.Process | None
        ) = None

        self._started_by_us = False

        self._start_lock = asyncio.Lock()

    async def start(self) -> None:
        """
        Ensure that the aria2 RPC endpoint is available.

        If an aria2 instance is already running, it is reused.
        Otherwise, aria2c is started when auto_start is enabled.
        """

        async with self._start_lock:

            if await self._probe.is_available():
                return

            if not self._auto_start:
                raise RuntimeError(
                    "aria2 RPC is not available and "
                    "automatic aria2c startup is disabled. "
                    "Start aria2c manually or enable "
                    "aria2.auto_start.",
                )

            executable = self._resolve_executable()

            process = await self._start_process(
                executable,
            )

            self._process = process
            self._started_by_us = True

            try:

                await self._wait_until_ready()

            except BaseException:

                await self._terminate_process()

                raise

    async def close(self) -> None:
        """
        Stop aria2c only when this launcher started it.
        """

        async with self._start_lock:
            await self._terminate_process()

        await self._probe.close()


    def _resolve_executable(self) -> str:
        """
        Resolve the aria2c executable.

        Supports both an absolute/explicit executable path and
        executables available through PATH.
        """

        candidate = self._executable.strip()

        if candidate:
            if os.path.exists(candidate):
                return candidate

            resolved = shutil.which(candidate)
            if resolved is not None:
                return resolved

        env_candidate = os.environ.get("ARIA2C_PATH")
        if env_candidate:
            env_candidate = env_candidate.strip()
            if os.path.exists(env_candidate):
                return env_candidate

            resolved = shutil.which(env_candidate)
            if resolved is not None:
                return resolved

        raise RuntimeError(
            self._build_installation_error(),
        )

    async def _start_process(
        self,
        executable: str,
    ) -> asyncio.subprocess.Process:

        command = [
            executable,
            "--enable-rpc=true",
            f"--rpc-listen-port={self._rpc_port}",
            "--log-level=notice",
        ]

        if self._rpc_secret is not None:
            command.append(
                f"--rpc-secret={self._rpc_secret}",
            )

        try:
            return await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )

        except FileNotFoundError as exc:
            raise RuntimeError(
                self._build_installation_error(),
            ) from exc

        except OSError as exc:
            raise RuntimeError(
                "Failed to start aria2c: "
                f"{exc}",
            ) from exc

    async def _wait_until_ready(self) -> None:

        loop = asyncio.get_running_loop()

        deadline = (
            loop.time()
            + self._startup_timeout
        )

        while True:

            if await self._probe.is_available():
                return

            process = self._process

            if (
                process is not None
                and process.returncode is not None
            ):
                raise RuntimeError(
                    "aria2c exited before its RPC "
                    "endpoint became available. "
                    f"Process exit code: "
                    f"{process.returncode}.",
                )

            remaining = deadline - loop.time()

            if remaining <= 0:
                raise TimeoutError(
                    "Timed out waiting for aria2 RPC "
                    f"endpoint: {self._rpc_url}",
                )

            await asyncio.sleep(
                min(0.2, remaining),
            )



    async def _terminate_process(self) -> None:

        process = self._process

        self._process = None

        if not self._started_by_us:
            return

        self._started_by_us = False

        if process is None:
            return

        if process.returncode is not None:
            return

        process.terminate()

        try:

            await asyncio.wait_for(
                process.wait(),
                timeout=5.0,
            )

        except asyncio.TimeoutError:

            process.kill()

            await process.wait()

    def _build_installation_error(self) -> str:

        env_path = os.environ.get("ARIA2C_PATH")

        return (
            "aria2c executable was not found. "
            "Aria2Downloader requires aria2c to be "
            "installed and available on PATH, or an explicit "
            "path must be configured via `application.aria2.executable` "
            "or the `ARIA2C_PATH` environment variable. "
            "Install aria2 and make sure the `aria2c` command is "
            "available from your terminal. "
            f"Configured executable: {self._executable!r}. "
            f"ARIA2C_PATH={env_path!r}."
        )