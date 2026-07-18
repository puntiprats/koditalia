import json

from pathlib import Path


CONFIG = Path("config") / "sources.json"

with open(CONFIG, encoding="utf8") as f:

    SOURCES = json.load(f)["sources"]


PRIORITY = {
    s["name"]: s["priority"]
    for s in SOURCES
}


def priority(channel):

    return PRIORITY.get(
        channel.source,
        0
    )