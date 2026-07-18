from dataclasses import dataclass


@dataclass
class Channel:

    extinf: str
    url: str

    name: str

    tvg_id: str = ""
    tvg_name: str = ""
    tvg_logo: str = ""
    group: str = ""