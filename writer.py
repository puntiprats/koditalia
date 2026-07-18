from models import Channel


def save_playlist(channels: list[Channel], filename: str):

    with open(filename, "w", encoding="utf8") as f:

        f.write("#EXTM3U\n")

        for c in channels:

            f.write(c.extinf + "\n")
            f.write(c.url + "\n")