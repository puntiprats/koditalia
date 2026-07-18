from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from collections import Counter
from parser import load_playlist


channels = load_playlist("sources/it.m3u", "iptv-org")


print(f"Canali: {len(channels)}")

print()

print("========== NOMI ==========")

names = sorted(set(c.name for c in channels))

for n in names:
    print(n)

print()

print("========== TVG-ID ==========")

ids = sorted(set(c.tvg_id for c in channels if c.tvg_id))

for i in ids:
    print(i)

print()

print("========== TVG-NAME ==========")

names = sorted(set(c.tvg_name for c in channels if c.tvg_name))

for n in names:
    print(n)

print()

print("========== DUPLICATI TVG-ID ==========")

counter = Counter(c.tvg_id for c in channels if c.tvg_id)

for key, value in sorted(counter.items()):

    if value > 1:

        print(value, key)