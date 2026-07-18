import urllib.request
import urllib.error
import time
import json
from pathlib import Path


CONFIG = json.load(
    open(
        Path("config") / "settings.json",
        encoding="utf8"
    )
)

CONFIG["user_agent"] = (
    "Mozilla/5.0 KodiItalia Builder"
)


CACHE = {}


def alive(url: str) -> bool:

    if url in CACHE:
        return CACHE[url]

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT
        }
    )

    try:

        with urllib.request.urlopen(
            request,
timeout=CONFIG["timeout"]
        ) as response:

            ok = response.status < 400

    except Exception:

        ok = False

    CACHE[url] = ok

    return ok