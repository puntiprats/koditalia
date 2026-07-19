from dataclasses import dataclass
from time import perf_counter
import requests

_CACHE = {}

@dataclass
class StreamStatus:
    alive: bool
    response_time: float | None
    status_code: int |None
    error: str | None


def check_stream(url: str, timeout: int = 5) -> StreamStatus:

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

        result = StreamStatus(
            alive=response.ok,
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