from pathlib import Path

from parser import load_playlist
from writer import save_playlist
from matcher import canonical_name
from lcn import channel_number
from quality import score


INPUT = "it.m3u"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "tvitalia.m3u"


def main():

    channels = load_playlist(INPUT)

    for c in channels:
        c.name = canonical_name(c.name)

    print(f"{len(channels)} canali caricati")

best = {}
duplicates = []

for c in channels:

    key = c.name

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

    if n is None:

        unknown.append(c)

    else:

        known.append((n, c))

known.sort(key=lambda x: x[0])

unknown.sort(key=lambda x: x.name)

ordered = [c for _, c in known]

ordered.extend(unknown)

save_playlist(ordered, OUTPUT)

    print("Playlist salvata in", OUTPUT)


if __name__ == "__main__":
    main()