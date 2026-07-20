from parser import load_playlist
from pipeline import normalize_channels
from selector import select_best
from sources import fetch
from pathlib import Path
from writer import write_playlist
from lcn import apply_lcn
from stats import print_sources

OUTPUT = Path("output") / "tvitalia.m3u"

def build():

    channels = []

    for source, filename in fetch():

        loaded = load_playlist(
            filename,
            source["name"]
        )

        channels.extend(loaded)
        
    channels = normalize_channels(channels)

    print_sources(channels)

    selected, duplicates = select_best(channels)

    selected = apply_lcn(selected)

    print()

    print("==========")

    print("Loaded :", len(channels))

    print("Selected :", len(selected))

    print("Duplicates :", len(duplicates))

    print()

    write_playlist(
        selected,
        duplicates,
        OUTPUT
    )

    return selected, duplicates