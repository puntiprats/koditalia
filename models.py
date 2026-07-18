from dataclasses import dataclass


@dataclass(slots=True)
class Channel:
    """
    Rappresenta un singolo stream trovato in una playlist M3U.
    Tutti i moduli lavoreranno esclusivamente su questa struttura.
    """

    # Informazioni originali
    name: str
    url: str
    extinf: str

    # Metadata IPTV
    tvg_id: str = ""
    tvg_name: str = ""
    tvg_logo: str = ""
    group_title: str = ""

    # Elaborazione
    source: str = ""
    source_priority: int = 0

    identity: str = ""
    quality_score: int = 0

    lcn: int | None = None