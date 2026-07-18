import json
from pathlib import Path

from utils import normalize


ALIASES_FILE = Path("config") / "aliases.json"


with open(ALIASES_FILE, encoding="utf8") as f:
    RAW = json.load(f)


ALIASES = {}

for canonical, aliases in RAW.items():

    ALIASES[normalize(canonical)] = canonical

    for alias in aliases:

        ALIASES[normalize(alias)] = canonical


def canonical_name(name: str) -> str:

    key = normalize(name)

    return ALIASES.get(key, name)