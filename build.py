from pathlib import Path

from parser import load_playlist
from writer import save_playlist
from matcher import canonical_name


INPUT = "it.m3u"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "tvitalia.m3u"


def main():

    channels = load_playlist(INPUT)

    for c in channels:
        c.name = canonical_name(c.name)

    print(f"{len(channels)} canali caricati")

    save_playlist(channels, OUTPUT)

    print("Playlist salvata in", OUTPUT)


if __name__ == "__main__":
    main()