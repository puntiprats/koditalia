from identity import build_identity
from quality import apply_quality

from models import Channel


def normalize_channels(
    channels: list[Channel]
) -> list[Channel]:

    for channel in channels:

        clean_name = channel.name.replace("Ⓖ", "").strip()

        channel.identity = build_identity(
            clean_name,
            channel.tvg_id,
            channel.tvg_name
        )

        if channel.identity in (
            "Canale 5",
            "Italia 1",
            "Rete 4",
        ):
            print(
                "DEBUG FINAL:",
                channel.name,
                "| identity:",
                channel.identity,
                "| tvg-id:",
                channel.tvg_id,
                "| source:",
                channel.source
            )

        channel.name = channel.identity

    apply_quality(channels)

    return channels