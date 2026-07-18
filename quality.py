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

    text = f"{channel.name} {channel.extinf}".lower()

    score = 0

    for pattern, value in RULES:

        if re.search(pattern, text):
            score = max(score, value)

    return score


def apply_quality(channels: list[Channel]) -> None:

    for channel in channels:

        channel.quality_score = calculate_quality(channel)