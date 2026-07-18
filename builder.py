from pathlib import Path

from parser import load_playlist
from writer import save_playlist

from matcher import canonical_name
from lcn import channel_number
from quality import score
from identity import channel_key
from validator import alive
from sources import fetch
from stats import print_sources


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "tvitalia.m3u"


def build():

    channels = []

    for source, playlist in fetch():

        loaded = load_playlist(
            playlist,
            source["name"]
        )

        channels.extend(loaded)

    print(f"{len(channels)} canali caricati")

    print_sources(channels)

    valid_channels = []

    for c in channels:

        if alive(c.url):

            valid_channels.append(c)

    channels = valid_channels

    print(f"{len(channels)} canali validi")

    for c in channels:

        c.name = canonical_name(c.name)

    best = {}

    duplicates = []

    for c in channels:

        key = channel_key(c)

        if key not in best:

            best[key] = c
            continue

        if score(c) > score(best[key]):

            duplicates.append(best[key])
            best[key] = c

        else:

            duplicates.append(c)

    known = []
    unknown = []

    for c in best.values():

        n = channel_number(c.name)

        c.lcn = n

        if n is None:

            unknown.append(c)

        else:

            known.append((n, c))

    known.sort(key=lambda x: x[0])

    unknown.sort(key=lambda x: x.name)

    ordered = [c for _, c in known]

    ordered.extend(unknown)

    duplicates.sort(
        key=lambda c: (
            c.name,
            -score(c)
        )
    )

    save_playlist(
        ordered,
        duplicates,
        OUTPUT
    )

    print()

    print("==============")

    print(f"Principali : {len(ordered)}")

    print(f"Duplicati  : {len(duplicates)}")

    print(f"Totale     : {len(channels)}")

    print()

    print("Output:", OUTPUT)