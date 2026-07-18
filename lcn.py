import json
from pathlib import Path

from models import Channel


with open(Path("config") / "lcn.json", encoding="utf8") as f:
    LCN = json.load(f)


def apply_lcn(channels: list[Channel]) -> list[Channel]:

    ordered = []
    extra = []

    for channel in channels:

        number = LCN.get(channel.identity)

        if number is None:
            extra.append(channel)
            continue

        channel.lcn = number
        ordered.append(channel)

    ordered.sort(key=lambda c: c.lcn)
    extra.sort(key=lambda c: c.identity.lower())

    return ordered + extra