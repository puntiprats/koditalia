import re

from models import Channel


NAME_RE = re.compile(r",(.*)$")
ATTR_RE = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')


def parse_channel(extinf: str, url: str) -> Channel:

    attrs = dict(ATTR_RE.findall(extinf))

    name = ""

    m = NAME_RE.search(extinf)

    if m:
        name = m.group(1).strip()

    return Channel(
        extinf=extinf,
        url=url.strip(),
        name=name,
        tvg_id=attrs.get("tvg-id", ""),
        tvg_name=attrs.get("tvg-name", ""),
        tvg_logo=attrs.get("tvg-logo", ""),
        group=attrs.get("group-title", "")
    )


def load_playlist(filename: str):

    channels = []

    with open(filename, encoding="utf8") as f:

        lines = [x.rstrip() for x in f.readlines()]

    i = 0

    while i < len(lines):

        line = lines[i]

        if line.startswith("#EXTINF"):

            if i + 1 < len(lines):

                channels.append(
                    parse_channel(
                        line,
                        lines[i + 1]
                    )
                )

                i += 2

                continue

        i += 1

    return channels