from models import Channel


def ranking(channel: Channel) -> tuple:

    force_user_agent = (
        "forceuseragent=" in channel.url.lower()
    )

    return (
        channel.alive,
        not channel.geo_blocked,
        force_user_agent,
        channel.source_priority,
        channel.quality_score,
        -(channel.response_time or 9999),
        channel.name.lower(),
    )