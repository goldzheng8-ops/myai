from __future__ import annotations
from dataclasses import dataclass, field

from core.request.context import RequestContext


@dataclass(frozen=True, slots=True)
class Aria2Options:

    dir: str | None = None

    out: str | None = None

    headers: tuple[str, ...] = ()

    cookies: tuple[str, ...] = ()

    proxy: str | None = None

    timeout: float | None = None

    connect_timeout: float | None = None

    max_tries: int | None = None

    retry_wait: float | None = None

    continue_download: bool = True

    allow_overwrite: bool = False

    auto_file_renaming: bool = False

    max_connection_per_server: int | None = None

    split: int | None = None

    min_split_size: str | None = None

    user_agent: str | None = None

    referer: str | None = None

    checksum: str | None = None

    extra: dict[str, str] = field(
        default_factory=dict,
    )

    def to_rpc_options(self) -> dict[str, str]:

        options: dict[str, str] = {}

        if self.dir is not None:
            options["dir"] = self.dir

        if self.out is not None:
            options["out"] = self.out

        if self.headers:
            options["header"] = ",".join(
                self.headers,
            )

        if self.cookies:
            options["cookie"] = "; ".join(
                self.cookies,
            )

        if self.proxy is not None:
            options["all-proxy"] = self.proxy

        if self.timeout is not None:
            options["timeout"] = str(
                int(self.timeout),
            )

        if self.connect_timeout is not None:
            options["connect-timeout"] = str(
                int(self.connect_timeout),
            )

        if self.max_tries is not None:
            options["max-tries"] = str(
                self.max_tries,
            )

        if self.retry_wait is not None:
            options["retry-wait"] = str(
                self.retry_wait,
            )

        options["continue"] = (
            "true"
            if self.continue_download
            else "false"
        )

        options["allow-overwrite"] = (
            "true"
            if self.allow_overwrite
            else "false"
        )

        options["auto-file-renaming"] = (
            "true"
            if self.auto_file_renaming
            else "false"
        )

        if (
            self.max_connection_per_server
            is not None
        ):
            options[
                "max-connection-per-server"
            ] = str(
                self.max_connection_per_server,
            )

        if self.split is not None:
            options["split"] = str(
                self.split,
            )

        if self.min_split_size is not None:
            options["min-split-size"] = (
                self.min_split_size
            )

        if self.user_agent is not None:
            options["user-agent"] = (
                self.user_agent
            )

        if self.referer is not None:
            options["referer"] = (
                self.referer
            )

        if self.checksum is not None:
            options["checksum"] = (
                self.checksum
            )

        options.update(self.extra)

        return options

class Aria2OptionsBuilder:

    def __init__(
        self,
        *,
        directory: str | None = None,
        timeout: float | None = None,
    ) -> None:

        self._directory = directory
        self._timeout = timeout

    def build(
        self,
        context: RequestContext,
    ) -> Aria2Options:

        descriptor = context.descriptor

        headers = tuple(
            f"{key}: {value}"
            for key, value
            in descriptor.headers.items()
        )

        cookies = tuple(
            f"{key}={value}"
            for key, value
            in descriptor.cookies.items()
        )

        proxy = None

        if descriptor.proxy is not None:
            proxy = descriptor.proxy.as_url()

        return Aria2Options(
            dir=self._directory,
            headers=headers,
            cookies=cookies,
            proxy=proxy,
            timeout=self._timeout,
        )