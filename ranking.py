from models import Channel


def ranking(channel: Channel) -> tuple:

    # True  = stream verificato funzionante
    # False = stream verificato non funzionante
    # None  = stream non ancora verificato
    alive_score = {
        True: 2,
        None: 1,
        False: 0,
    }.get(channel.alive, 0)

    return (
        alive_score,
        not channel.geo_blocked,
        channel.source_priority,
        channel.quality_score,
        -(channel.response_time or 9999),
        channel.name.lower(),
    )