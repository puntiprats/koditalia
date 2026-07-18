from models import Channel


def ranking(channel: Channel) -> tuple:

    """
    Restituisce il ranking del canale.

    L'ordinamento è:

    1) priorità sorgente
    2) qualità video
    3) nome (solo per stabilità del sort)
    """

    return (
        channel.source_priority,
        channel.quality_score,
        channel.name.lower()
    )