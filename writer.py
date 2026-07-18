from models import Channel


def _renumber(channel: Channel, number: int) -> str:

    extinf = channel.extinf

    if f'tvg-chno="' in extinf:

        import re
        extinf = re.sub(r'tvg-chno="[^"]*"', f'tvg-chno="{number}"', extinf)

    else:

        pos = extinf.find(",")

        extinf = extinf[:pos] + f' tvg-chno="{number}"' + extinf[pos:]

    return extinf


def save_playlist(channels: list[Channel], duplicates: list[Channel], filename: str):

    with open(filename, "w", encoding="utf8") as f:

        f.write("#EXTM3U\n")

        for c in channels:

            f.write(c.extinf + "\n")
            f.write(c.url + "\n")

        ch = 800

        for c in duplicates:

            extinf = _renumber(c, ch)

            f.write(extinf + "\n")
            f.write(c.url + "\n")

            ch += 1