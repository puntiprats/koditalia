import re

from matcher import canonical_name


def build_identity(name: str, tvg_id: str = "", tvg_name: str = "") -> str:
    """
    Restituisce l'identità canonica del canale.

    L'ordine di priorità è:
    1. Nome del canale
    2. tvg-name
    3. tvg-id
    """

    candidate = name

    if not candidate and tvg_name:
        candidate = tvg_name

    if not candidate and tvg_id:
        candidate = tvg_id

    candidate = candidate.strip()

    # rimuove eventuale suffisso qualità
    candidate = re.sub(
        r'@(?:sd|hd|fhd|uhd|4k)$',
        '',
        candidate,
        flags=re.IGNORECASE
    )

    # rimuove suffisso .it
    candidate = re.sub(
        r'\.it$',
        '',
        candidate,
        flags=re.IGNORECASE
    )
    
    # Inserisce uno spazio tra lettere e numeri
    candidate = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', candidate)

    candidate = candidate.strip()

    # Eccezioni italiane
    candidate = re.sub(r'^La\s+7$', 'LA7', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Tv\s+8$', 'TV8', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Rai\s+1$', 'Rai 1', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Rai\s+2$', 'Rai 2', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Rai\s+3$', 'Rai 3', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Rete\s+4$', 'Rete 4', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Canale\s+5$', 'Canale 5', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'^Italia\s+1$', 'Italia 1', candidate, flags=re.IGNORECASE)

    return canonical_name(candidate)