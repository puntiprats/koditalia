from parser import load_playlist
from pipeline import normalize_channels
from selector import select_best
from sources import fetch
from pathlib import Path
from writer import write_playlist
from lcn import apply_lcn

OUTPUT = Path("output") / "tvitalia.m3u"

def build():

    channels = []

    for source, filename in fetch():

        loaded = load_playlist(
            filename,
            source["name"]
        )

        channels.extend(loaded)
        
    print("\n=== PLAYLIST LOADED ===")

    for c in channels:
        if (
            "Canale" in c.tvg_id
            or "Italia" in c.tvg_id
            or "Rete" in c.tvg_id
        ):
            print(
                c.tvg_id,
                "|",
                c.name,
                "|",
                c.tvg_name
            )


    channels = normalize_channels(channels)
    print("\n=== PRIME 30 IDENTITY ===")

    for c in channels[:30]:
        print(
            "NAME:", c.name,
            "| TVG-ID:", c.tvg_id,
            "| IDENTITY:", c.identity
        )
        
    for c in channels:
        if "Canale" in c.name or "Italia" in c.name or "Rete" in c.name:
            print(c.name, "->", c.identity)

    selected, duplicates = select_best(channels)

    print("\nSELECTED\n")

    for c in selected:
        if c.identity in (
            "Canale 5",
            "Italia 1",
            "Rete 4",
        ):
            print(c.identity)

    selected = apply_lcn(selected)

    print("\n=== MEDIASET ===")

    for c in selected:
        if c.identity in (
            "Rete 4",
            "Canale 5",
            "Italia 1",
            "LA7",
            "TV8",
            "Nove",
        ):
            print(c.identity, "LCN =", c.lcn)

    print("\nLCN\n")

    for c in selected[:15]:
        print(c.lcn, c.identity)

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