import json
from pathlib import Path

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

META = CACHE_DIR / "metadata.json"


def load():

    if not META.exists():
        return {}

    with open(META, encoding="utf8") as f:
        return json.load(f)


def save(data):

    with open(META, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


metadata = load()