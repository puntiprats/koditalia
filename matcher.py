import json

from pathlib import Path

from utils import normalize


ALIASES_FILE = Path("config") / "aliases.json"


def load_aliases():

    if not ALIASES_FILE.exists():
        return {}

    with open(ALIASES_FILE, encoding="utf8") as f:

        raw = json.load(f)

    aliases = {}

    for canonical, names in raw.items():

        aliases[normalize(canonical)] = canonical

        for n in names:
            aliases[normalize(n)] = canonical

    return aliases


ALIASES = load_aliases()


def canonical_name(name: str) -> str:

    key = normalize(name)

    return ALIASES.get(key, name)