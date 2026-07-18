import json

from pathlib import Path


LCN_FILE = Path("config") / "lcn.json"


def load_lcn():

    with open(LCN_FILE, encoding="utf8") as f:
        return json.load(f)


LCN = load_lcn()


def channel_number(name: str):

    return LCN.get(name)