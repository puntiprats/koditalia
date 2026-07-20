from dataclasses import dataclass
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from config import settings
import requests

_CACHE = {}

@dataclass
class StreamStatus:
    alive: bool
    response_time: float | None
    status_code: int |None
    error: str | None


def check_stream(url: str, timeout=None) -> StreamStatus:

    if timeout is None:
        timeout = settings["timeout"]

    if url in _CACHE:
        return _CACHE[url]

    start = perf_counter()

    try:

        response = requests.get(
            url,
            stream=True,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "KodiItalia/1.0"
                )
            },
        )

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        alive = (
            response.ok
            and (
                "mpegurl" in content_type
                or "application/vnd.apple.mpegurl" in content_type
                or url.endswith(".m3u8")
            )
        )

        result = StreamStatus(
            alive=alive,
            response_time=perf_counter() - start,
            status_code=response.status_code,
            error=None,
        )

        _CACHE[url] = result

        return result

    except Exception as exc:

        result = StreamStatus(
            alive=False,
            response_time=None,
            status_code=None,
            error=str(exc),
        )

        _CACHE[url] = result

        return result


def check_streams(
    channels,
    workers: int = 10,
):

    with ThreadPoolExecutor(max_workers=workers) as executor:

        results = executor.map(
            lambda c: (c, check_stream(c.url)),
            channels,
        )

        for channel, status in results:

            channel.alive = status.alive
            channel.response_time = status.response_time
            channel.status_code = status.status_code

    return channels