from dataclasses import dataclass
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests
import re

QUALITY_RE = re.compile(r"RESOLUTION=(\d+)x(\d+)")

_CACHE = {}


@dataclass
class StreamStatus:
    alive: bool
    geo_blocked: bool
    response_time: float | None
    status_code: int | None
    error: str | None
    quality: int | None


def verify_hls(response, url: str) -> bool:

    try:

        content = response.text[:10000]

        if "#EXTM3U" not in content:
            return False

        if "#EXT-X-STREAM-INF" in content:
            return True

        if "#EXTINF:" in content:
            return True

        return False

    except Exception:

        return False


def check_stream(url: str, timeout=None) -> StreamStatus:

    if timeout is None:
        timeout = 5

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

        quality = detect_quality(response)

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

        # Per gli stream HLS, verifica che la risposta
        # contenga effettivamente un manifest M3U8 valido.
        if alive and (
            ".m3u8" in url.lower()
            or "mpegurl" in content_type
        ):

            alive = verify_hls(
                response,
                url
            )

        result = StreamStatus(
            alive=alive,
            geo_blocked=geo_blocked,
            response_time=perf_counter() - start,
            status_code=status,
            error=None,
            quality=quality,
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
            quality=None,
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
            
        if status.quality is not None:

            channel.quality_score = max(
                channel.quality_score,
                status.quality
            )

        if "forceuseragent=" in channel.url.lower():

            channel.quality_score += 50

    return channels


def detect_quality(response) -> int | None:

    try:

        text = response.text[:10000]

    except Exception:

        return None

    match = QUALITY_RE.search(text)

    if not match:
        return None

    height = int(match.group(2))

    if height >= 1080:
        return 100

    if height >= 720:
        return 80

    if height >= 576:
        return 60

    if height >= 480:
        return 40

    return 20