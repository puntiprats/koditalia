from matcher import canonical_name
from quality import apply_quality

from models import Channel


def normalize_channels(channels: list[Channel]) -> list[Channel]:

    for channel in channels:

        channel.canonical_name = canonical_name(
            channel.name
        )

    apply_quality(channels)

    return channels