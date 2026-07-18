import re
import unicodedata


QUALITY_WORDS = [
    "uhd",
    "ultrahd",
    "4k",
    "2160",
    "fhd",
    "fullhd",
    "1080",
    "hd",
    "720",
    "576",
    "sd",
    "hevc",
    "h265",
    "h264",
    "mpeg4",
    "av1",
    "backup",
    "test",
    "hq"
]


def normalize(text: str) -> str:

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode()

    text = text.lower()

    for word in QUALITY_WORDS:
        text = text.replace(word, " ")

    text = text.replace("+", " ")

    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)

    text = re.sub(r"[^a-z0-9]+", " ", text)

    text = " ".join(text.split())

    return text