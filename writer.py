import re
from pathlib import Path

from models import Channel


def set_channel_number(extinf: str, number: int) -> str:

    if 'tvg-chno="' in extinf:

        return re.sub(
            r'tvg-chno="[^"]*"',
            f'tvg-chno="{number}"',
            extinf
        )

    comma = extinf.find(",")

    if comma == -1:
        return extinf

    return (
        extinf[:comma]
        + f' tvg-chno="{number}"'
        + extinf[comma:]
    )


def write_playlist(
    channels: list[Channel],
    duplicates: list[Channel],
    filename: Path,
):

    filename.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(filename, "w", encoding="utf8") as f:

        f.write("#EXTM3U\n")

        for channel in channels:

            extinf = channel.extinf

            if channel.lcn is not None:

                extinf = set_channel_number(
                    extinf,
                    channel.lcn
                )

            f.write(extinf + "\n")
            f.write(channel.url + "\n")

        duplicate_number = 800

        for channel in duplicates:

            extinf = set_channel_number(
                channel.extinf,
                duplicate_number
            )

            f.write(extinf + "\n")
            f.write(channel.url + "\n")

            duplicate_number += 1