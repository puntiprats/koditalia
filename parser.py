import re

from models import Channel


ATTR_RE = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')


def parse_extinf(line: str) -> tuple[dict[str, str], str]:
    """
    Estrae gli attributi di una riga EXTINF e il nome del canale.
    """

    attrs = dict(ATTR_RE.findall(line))

    if "," in line:
        name = line.rsplit(",", 1)[1].strip()
    else:
        name = ""

    return attrs, name


def load_playlist(filename: str, source: str) -> list[Channel]:
    """
    Carica una playlist M3U e restituisce una lista di Channel.
    """

    channels: list[Channel] = []

    with open(filename, encoding="utf8") as f:
        lines = [line.strip() for line in f]

    i = 0

    while i < len(lines):

        line = lines[i]

        if not line.startswith("#EXTINF"):
            i += 1
            continue

        if i + 1 >= len(lines):
            break

        user_agent = ""

        j = i + 1

        while j < len(lines) and lines[j].startswith("#"):

            if lines[j].startswith("#EXTVLCOPT:http-user-agent="):
                user_agent = lines[j].split("=", 1)[1]

            j += 1


        if j >= len(lines):
            break


        url = lines[j].strip()

        attrs, name = parse_extinf(line)

        channels.append(
            Channel(
                name=name,
                url=url,
                extinf=line,
                tvg_id=attrs.get("tvg-id", ""),
                tvg_name=attrs.get("tvg-name", ""),
                tvg_logo=attrs.get("tvg-logo", ""),
                group_title=attrs.get("group-title", ""),
                source=source,
                user_agent=user_agent
            )
        )

        i = j + 1

    return channels