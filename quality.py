import re
from priority import priority


SCORES = [
    ("2160", 250),
    ("uhd", 240),
    ("4k", 230),

    ("1080", 200),
    ("fhd", 190),

    ("720", 150),
    ("hd", 140),

    ("576", 80),
    ("sd", 70),

    ("backup", -150),
    ("test", -200)
]


def score(channel):

    text = channel.extinf.lower()

    total = 0

    for word, value in SCORES:

        if re.search(r"\b" + re.escape(word) + r"\b", text):

            total += value

return total + priority(channel)