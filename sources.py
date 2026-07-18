import json
import urllib.request

from pathlib import Path


CONFIG = Path("config") / "sources.json"

CACHE = Path("cache")

CACHE.mkdir(exist_ok=True)


def load_sources():

    with open(CONFIG, encoding="utf8") as f:
        return json.load(f)["sources"]


def download(name: str, url: str):

    filename = CACHE / f"{name}.m3u"

    urllib.request.urlretrieve(url, filename)

    return filename


def fetch():

    playlists = []

    for source in load_sources():

        if not source["enabled"]:
            continue

        filename = download(
            source["name"],
            source["url"]
        )

        playlists.append(
            (
                source,
                filename
            )
        )

    return playlists