import re

from matcher import canonical_name


# Suffissi che non devono influire sull'identità del canale.
QUALITY_SUFFIX_RE = re.compile(
    r"""
    \s*
    (?:
        \(\s*(?:576p|720p|1080p|2160p|4k|uhd|hd|fhd|sd)\s*\)
        |
        \[\s*(?:geo-blocked|geo blocked)\s*\]
        |
        \b(?:576p|720p|1080p|2160p|4k|uhd|fhd|hd|sd)\b
    )
    \s*$
    """,
    flags=re.IGNORECASE | re.VERBOSE,
)


def clean_candidate(value: str) -> str:

    value = value.strip()

    # Rimuove simboli Free-TV come Ⓖ
    value = value.replace("Ⓖ", "")

    # Rimuove suffissi geo-blocking
    value = re.sub(
        r"\s*\[\s*geo[- ]?blocked\s*\]",
        "",
        value,
        flags=re.IGNORECASE,
    )

    # Rimuove eventuali suffissi di qualità ripetuti.
    # Esempi:
    # Rai 1 (576p)
    # Rai 2 HD
    # Rai 3 (1080p)
    # DMAX HD
    for _ in range(3):

        cleaned = QUALITY_SUFFIX_RE.sub(
            "",
            value,
        ).strip()

        if cleaned == value:
            break

        value = cleaned

    # Rimuove suffisso @SD / @HD / @FHD / @UHD / @4K
    value = re.sub(
        r"@(?:sd|hd|fhd|uhd|4k)$",
        "",
        value,
        flags=re.IGNORECASE,
    )

    # Rimuove suffisso .it
    value = re.sub(
        r"\.it$",
        "",
        value,
        flags=re.IGNORECASE,
    )


    # Normalizza punti usati nei tvg-id
    # Esempio:
    # Canale.5 -> Canale 5
    # Italia.1 -> Italia 1
    # Rete.4 -> Rete 4

    value = re.sub(
        r"\.",
        " ",
        value,
    )


    # Inserisce uno spazio tra lettere e numeri.
    # Esempio:
    # Rai1 -> Rai 1
    # DMAX24 -> DMAX 24
    value = re.sub(
        r"([A-Za-z])([0-9])",
        r"\1 \2",
        value,
    )

    # Normalizzazione degli spazi
    value = re.sub(
        r"\s+",
        " ",
        value,
    ).strip()

    return value


def build_identity(
    name: str,
    tvg_id: str = "",
    tvg_name: str = "",
) -> str:

    """
    Restituisce l'identità canonica del canale.

    Priorità:
    1. nome visualizzato
    2. tvg-name
    3. tvg-id
    """

    candidates = (
        name,
        tvg_name,
        tvg_id,
    )

    candidate = ""

    for value in candidates:

        if value and value.strip():

            candidate = value.strip()

            break

    if not candidate:

        return ""

    candidate = clean_candidate(
        candidate
    )

    # Eccezioni e nomi canonici italiani.
    aliases = {

        "la 7": "LA7",
        "la7": "LA7",

        "tv 8": "TV8",
        "tv8": "TV8",

        "nove": "Nove",

        "dmax": "DMAX",

        "rai 1": "Rai 1",
        "rai 2": "Rai 2",
        "rai 3": "Rai 3",

        "rete 4": "Rete 4",
        "canale 5": "Canale 5",
        "italia 1": "Italia 1",

        "la7d": "La7d",

        "rai movie": "Rai Movie",
        "rai premium": "Rai Premium",

        "cielo": "Cielo",

        "twentyseven": "Twentyseven",

        "tv2000": "TV2000",

        "real time": "Real Time",

        "food network": "Food Network",

        "warner tv": "Warner TV",

        "giallo": "Giallo",

        "top crime": "Top Crime",

        "boing": "Boing",

        "k2": "K2",

        "rai gulp": "Rai Gulp",
        "rai yoyo": "Rai YoYo",

        "frisbee": "Frisbee",

        "cartoonito": "Cartoonito",

        "super!": "Super!",

        "dmax": "DMAX",
    }

    key = candidate.lower()

    candidate = aliases.get(
        key,
        candidate,
    )

    return canonical_name(
        candidate
    )