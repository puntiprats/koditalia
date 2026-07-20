from dataclasses import dataclass
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from config import settings
import requests
import json
from pathlib import Path

_CACHE = {}


CACHE_FILE = Path("cache/stream_health.json")


def load_cache():

    if CACHE_FILE.exists():

        with CACHE_FILE.open(
            "r",
            encoding="utf8"
        ) as f:

            return json.load(f)

    return {}


def save_cache():

    CACHE_FILE.parent.mkdir(
        exist_ok=True
    )

    with CACHE_FILE.open(
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            _CACHE,
            f,
            indent=4
        )


_CACHE = load_cache()


@dataclass
class StreamStatus:
    alive: bool
    geo_blocked: bool
    response_time: float | None
    status_code: int | None
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

        status = response.status_code

        alive = (
            status == 200
        )

        geo_blocked = (
            status == 403
        )

        result = StreamStatus(
            alive=alive,
            geo_blocked=geo_blocked,
            response_time=perf_counter() - start,
            status_code=status,
            error=None,
        )

        _CACHE[url] = result

        return result

    except Exception as exc:

        result = StreamStatus(
            alive=False,
            geo_blocked=False,
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
            channel.geo_blocked = status.geo_blocked
            channel.response_time = status.response_time
            channel.status_code = status.status_code

    save_cache()

    return channels