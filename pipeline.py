from identity import build_identity
from quality import apply_quality

from models import Channel


def normalize_channels(channels: list[Channel]) -> list[Channel]:

    for channel in channels:

        channel.identity = build_identity(
            channel.name,
            channel.tvg_id,
            channel.tvg_name
        )
        
        if "Canale" in channel.tvg_id or "Italia" in channel.tvg_id or "Rete" in channel.tvg_id:
            print(
                f"""
        NAME      : {channel.name}
        TVG-ID    : {channel.tvg_id}
        TVG-NAME  : {channel.tvg_name}
        IDENTITY  : {channel.identity}
        """
            )

    apply_quality(channels)

    return channels