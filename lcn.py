import json
from pathlib import Path

from models import Channel


with open(
    Path("config") / "lcn.json",
    encoding="utf8"
) as f:

    LCN = json.load(f)


LCN = {
    key.lower(): value
    for key, value in LCN.items()
}


def apply_lcn(
    channels: list[Channel]
) -> list[Channel]:

    ordered = []
    extra = []

    for channel in channels:

        number = LCN.get(
            channel.identity.lower()
        )

        if number is None:

            extra.append(channel)

            continue

        channel.lcn = number

        ordered.append(channel)

    # Canali con LCN:
    # ordinamento numerico
    ordered.sort(
        key=lambda c: c.lcn
    )

    # Canali senza LCN:
    # NON devono interrompere la sequenza
    # dei canali nazionali.
    #
    # Li lasciamo dopo i canali LCN,
    # ordinati alfabeticamente.
    extra.sort(
        key=lambda c: (
            c.group_title.lower(),
            c.name.lower(),
        )
    )

    return ordered + extra