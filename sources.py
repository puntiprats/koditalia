import json
import urllib.request
import urllib.error

from cache import metadata, save
from pathlib import Path


CONFIG = Path("config") / "sources.json"

CACHE = Path("cache")

CACHE.mkdir(exist_ok=True)


def load_sources():

    with open(CONFIG, encoding="utf8") as f:
        return json.load(f)["sources"]


def download(name: str, url: str):

    filename = CACHE / f"{name}.m3u"

    headers = {}

    if name in metadata:

        if metadata[name].get("etag"):
            headers["If-None-Match"] = metadata[name]["etag"]

        if metadata[name].get("last_modified"):
            headers["If-Modified-Since"] = metadata[name]["last_modified"]

    request = urllib.request.Request(
        url,
        headers=headers
    )

    try:

        response = urllib.request.urlopen(request)

        with open(filename, "wb") as f:
            f.write(response.read())

        metadata[name] = {
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified")
        }

        save(metadata)

    except urllib.error.HTTPError as e:

        if e.code != 304:
            raise

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