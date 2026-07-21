import re

from models import Channel


RULES = (
    (r"\b2160\b", 500),
    (r"\b4k\b", 500),
    (r"\buhd\b", 500),

    (r"\b1080\b", 400),
    (r"\bfhd\b", 400),

    (r"\b720\b", 300),
    (r"\bhd\b", 300),

    (r"\b576\b", 200),
    (r"\bsd\b", 100),
)


def calculate_quality(channel: Channel) -> int:

    text = (
        f"{channel.name} "
        f"{channel.extinf} "
        f"{channel.url}"
    ).lower()

    score = 0

    for pattern, value in RULES:

        if re.search(pattern, text):
            score = max(
                score,
                value
            )

    # Alcuni stream utilizzano parametri URL
    # necessari per ottenere una variante
    # specifica del flusso.
    if "forceuseragent=" in channel.url.lower():

        score += 50

    return score


def apply_quality(
    channels: list[Channel]
) -> None:

    for channel in channels:

        channel.quality_score = calculate_quality(
            channel
        )

        print(
            "QUALITY DEBUG:",
            channel.url,
            "=>",
            channel.quality_score
        )