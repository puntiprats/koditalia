from dataclasses import dataclass
from time import perf_counter

import requests


@dataclass
class StreamStatus:

    alive: bool
    response_time: float | None
    status_code: int | None
    error: str | None


def check_stream(
    url: str,
    timeout: int = 5,
) -> StreamStatus:

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

        elapsed = perf_counter() - start

        return StreamStatus(
            alive=response.ok,
            response_time=elapsed,
            status_code=response.status_code,
            error=None,
        )

    except Exception as exc:

        return StreamStatus(
            alive=False,
            response_time=None,
            status_code=None,
            error=str(exc),
        )