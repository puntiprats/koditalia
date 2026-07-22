from models import Channel


def is_rai_channel(channel: Channel) -> bool:
    text = (
        f"{channel.name} "
        f"{channel.tvg_name} "
        f"{channel.url}"
    ).lower()

    return (
        "rai " in text
        or "rai1" in text
        or "rai2" in text
        or "rai3" in text
        or "rai 1" in text
        or "rai 2" in text
        or "rai 3" in text
    )


def has_rai_user_agent(channel: Channel) -> bool:
    return (
        "forceuseragent=rainet" in channel.url.lower()
    )


def special_score(channel: Channel) -> int:

    if (
        is_rai_channel(channel)
        and has_rai_user_agent(channel)
    ):
        return 1000

    return 0


def ranking(channel: Channel) -> tuple:

    alive_score = {
        True: 2,
        None: 1,
        False: 0,
    }.get(channel.alive, 0)

    return (
        alive_score,
        not channel.geo_blocked,
        special_score(channel),
        channel.source_priority,
        channel.quality_score,
        -(channel.response_time or 9999),
        channel.name.lower(),
    )