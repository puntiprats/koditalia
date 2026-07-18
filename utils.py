import re
import unicodedata


REMOVE_WORDS = {
    "hd",
    "fhd",
    "uhd",
    "4k",
    "sd",
    "1080",
    "720",
    "2160",
    "backup",
    "test",
    "hevc",
    "h265",
    "h264",
    "mpeg4",
    "av1"
}


def normalize(text: str) -> str:

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode()

    text = text.lower()

    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)

    text = re.sub(r"[^a-z0-9]+", " ", text)

    words = []

    for word in text.split():

        if word not in REMOVE_WORDS:

            words.append(word)

    return " ".join(words)