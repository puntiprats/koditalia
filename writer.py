import re
from pathlib import Path

from models import Channel


def remove_channel_number(extinf: str) -> str:

    return re.sub(
        r'\s*tvg-chno="[^"]*"',
        "",
        extinf
    )


def clean_display_name(extinf: str) -> str:

    # Rimuove il simbolo Free-TV Ⓖ dal nome visualizzato
    extinf = re.sub(
        r'\s*Ⓖ',
        '',
        extinf
    )

    # Rimuove eventuali varianti "(G)"
    extinf = re.sub(
        r'\s*\(G\)',
        '',
        extinf,
        flags=re.IGNORECASE
    )

    return extinf


def set_channel_number(
    extinf: str,
    number: int
) -> str:

    extinf = remove_channel_number(
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

    with open(
        filename,
        "w",
        encoding="utf8"
    ) as f:

        f.write("#EXTM3U\n")

        for channel in channels:

            extinf = clean_display_name(
                channel.extinf
            )

            if channel.lcn is not None:

                extinf = set_channel_number(
                    extinf,
                    channel.lcn
                )

            else:

                extinf = remove_channel_number(
                    extinf
                )

            f.write(
                extinf + "\n"
            )

            f.write(
                channel.url + "\n"
            )

        duplicate_number = 800

        for channel in duplicates:

            extinf = clean_display_name(
                channel.extinf
            )

            extinf = set_channel_number(
                extinf,
                duplicate_number
            )
            
            f.write(
                extinf + "\n"
            )

            f.write(
                channel.url + "\n"
            )

            duplicate_number += 1