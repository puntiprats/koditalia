from parser import load_playlist
from pipeline import normalize_channels
from selector import select_best
from sources import fetch
from pathlib import Path
from writer import write_playlist
from lcn import apply_lcn
from stats import print_sources
from stats import print_selected

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

    print()

    print("===== CHECK NATIONAL =====")

    CHECK_CHANNELS = (
        "rai 1",
        "rai 3",
        "rete 4",
        "canale 5",
        "italia 1",
        "tv8",
        "la7",
        "nove",
    )

    for channel in selected + duplicates:

        if channel.identity.lower() in CHECK_CHANNELS:

            print(
                channel.name,
                "|",
                channel.identity,
                "|",
                channel.url,
                "| alive:",
                channel.alive,
                "| geo:",
                channel.geo_blocked,
                "| quality:",
                channel.quality_score,
                "| response:",
                channel.response_time,
                "| status:",
                channel.status_code,
                "| selected:",
                channel in selected,
            )

    print_selected(selected)

    selected = apply_lcn(selected)

    print()

    print("===== FIRST 30 =====")

    for channel in selected[:30]:

        print(
            channel.lcn,
            "|",
            channel.name,
            "|",
            channel.identity
        )

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