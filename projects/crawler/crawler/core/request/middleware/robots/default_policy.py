import asyncio
import time

from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

from core.request.middleware.robots.cache import RobotsCacheEntry
from core.request.middleware.robots.exceptions import RobotsFetchError
from core.request.middleware.robots.policy import RobotsPolicy
from core.request.middleware.robots.typing import RobotsFailureStrategy
import httpx




class DefaultRobotsPolicy(
    RobotsPolicy,
):

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        ttl: float = 3600.0,
        failure_strategy: RobotsFailureStrategy = (
            RobotsFailureStrategy.ALLOW
        ),
        failure_ttl: float = 60.0,
    ) -> None:

        self._timeout = timeout
        self._ttl = ttl
        self._failure_strategy = failure_strategy
        self._failure_ttl = failure_ttl

        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        )

        self._cache: dict[
            str,
            RobotsCacheEntry,
        ] = {}

        self._in_flight: dict[
            str,
            asyncio.Future[RobotsCacheEntry],
        ] = {}

        self._lock = asyncio.Lock()

        self._closed = False

    async def allowed(
        self,
        *,
        url: str,
        user_agent: str,
    ) -> bool:

        origin = self._origin(url)

        entry = await self._get_entry(
            origin,
        )

        return entry.parser.can_fetch(
            user_agent,
            url,
        )

    async def _get_entry(
        self,
        origin: str,
    ) -> RobotsCacheEntry:

        now = time.monotonic()

        async with self._lock:

            entry = self._cache.get(
                origin,
            )

            if (
                entry is not None
                and entry.expires_at > now
            ):
                return entry

            future = self._in_flight.get(
                origin,
            )

            if future is None:

                future = asyncio.get_running_loop().create_future()

                self._in_flight[origin] = future

                owner = True

            else:

                owner = False

        if not owner:

            return await asyncio.shield(
                future,
            )

        try:

            entry = await self._fetch(
                origin,
            )

        except asyncio.CancelledError:

            async with self._lock:

                current = self._in_flight.get(
                    origin,
                )

                if current is future:
                    del self._in_flight[origin]

                    if not future.done():
                        future.cancel()

            raise

        except Exception as exc:

            try:

                entry = self._handle_failure(
                    origin=origin,
                    error=exc,
                )

            except Exception as failure_exc:

                async with self._lock:

                    current = self._in_flight.get(
                        origin,
                    )

                    if current is future:
                        del self._in_flight[origin]

                        if not future.done():
                            future.set_exception(
                                failure_exc,
                            )

                raise

        async with self._lock:

            self._cache[origin] = entry

            current = self._in_flight.get(
                origin,
            )

            if current is future:

                del self._in_flight[origin]

                if not future.done():
                    future.set_result(
                        entry,
                    )

        return entry

    async def _fetch(
        self,
        origin: str,
    ) -> RobotsCacheEntry:

        robots_url = f"{origin}/robots.txt"

        try:

            response = await self._client.get(
                robots_url,
            )

            response.raise_for_status()

        except httpx.HTTPStatusError as exc:

            if exc.response.status_code == 404:

                return self._empty_entry(
                    ttl=self._ttl,
                )

            raise RobotsFetchError(
                f"Failed to fetch robots.txt: "
                f"url={robots_url!r}, "
                f"status={exc.response.status_code}",
            ) from exc

        except httpx.HTTPError as exc:

            raise RobotsFetchError(
                f"Failed to fetch robots.txt: "
                f"url={robots_url!r}",
            ) from exc

        parser = RobotFileParser()

        parser.set_url(
            robots_url,
        )

        parser.parse(
            response.text.splitlines(),
        )

        return RobotsCacheEntry(
            parser=parser,
            expires_at=(
                time.monotonic()
                + self._ttl
            ),
        )

    def _handle_failure(
        self,
        *,
        origin: str,
        error: Exception,
    ) -> RobotsCacheEntry:

        strategy = self._failure_strategy

        if strategy is RobotsFailureStrategy.RAISE:
            raise RobotsFetchError(
                f"Unable to load robots.txt "
                f"for {origin!r}.",
            ) from error

        if strategy is RobotsFailureStrategy.DENY:
            return self._deny_entry(
                ttl=self._failure_ttl,
            )

        return self._allow_entry(
            ttl=self._failure_ttl,
        )

    @staticmethod
    def _empty_entry(
        *,
        ttl: float,
    ) -> RobotsCacheEntry:

        parser = RobotFileParser()

        parser.parse([])

        return RobotsCacheEntry(
            parser=parser,
            expires_at=(
                time.monotonic()
                + ttl
            ),
        )

    @staticmethod
    def _allow_entry(
        *,
        ttl: float,
    ) -> RobotsCacheEntry:

        parser = RobotFileParser()

        parser.parse([
            "User-agent: *",
            "Allow: /",
        ])

        return RobotsCacheEntry(
            parser=parser,
            expires_at=(
                time.monotonic()
                + ttl
            ),
        )

    @staticmethod
    def _deny_entry(
        *,
        ttl: float,
    ) -> RobotsCacheEntry:

        parser = RobotFileParser()

        parser.parse([
            "User-agent: *",
            "Disallow: /",
        ])

        return RobotsCacheEntry(
            parser=parser,
            expires_at=(
                time.monotonic()
                + ttl
            ),
        )

    @staticmethod
    def _origin(
        url: str,
    ) -> str:

        parts = urlsplit(url)

        if not parts.scheme or not parts.netloc:
            raise ValueError(
                f"Invalid URL: {url!r}",
            )

        return (
            f"{parts.scheme}://"
            f"{parts.netloc}"
        )

    async def close(self) -> None:

        if self._closed:
            return

        self._closed = True

        async with self._lock:

            futures = tuple(
                self._in_flight.values(),
            )

            self._in_flight.clear()

            for future in futures:

                if not future.done():
                    future.cancel()

        await self._client.aclose()