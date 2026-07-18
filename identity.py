from utils import normalize


def channel_key(channel):

    if channel.tvg_id:

        return channel.tvg_id.strip().lower()

    return normalize(channel.name)