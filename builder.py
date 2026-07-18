from parser import load_playlist
from pipeline import normalize_channels
from selector import select_best

from sources import fetch


def build():

    channels = []

    for source, filename in fetch():

        loaded = load_playlist(
            filename,
            source["name"]
        )

        channels.extend(loaded)

    channels = normalize_channels(channels)

    selected, duplicates = select_best(channels)

    print()

    print("==========")

    print("Loaded :", len(channels))

    print("Selected :", len(selected))

    print("Duplicates :", len(duplicates))

    print()

    return selected, duplicates