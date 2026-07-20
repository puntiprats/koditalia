from models import Channel


def ranking(channel: Channel) -> tuple:

    return (
        channel.alive,
        channel.geo_blocked,
        channel.source_priority,
        channel.quality_score,
        -(channel.response_time or 9999),
        channel.name.lower(),
    )