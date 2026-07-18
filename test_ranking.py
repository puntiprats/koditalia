from models import Channel
from ranking import ranking


a = Channel(
    name="HD",
    url="",
    extinf="",
    quality_score=300,
    source_priority=100
)

b = Channel(
    name="FHD",
    url="",
    extinf="",
    quality_score=400,
    source_priority=50
)

assert ranking(a) > ranking(b)

print("Ranking OK")