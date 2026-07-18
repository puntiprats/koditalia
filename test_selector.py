from models import Channel

from selector import select_best


channels = [

    Channel(
        name="Rai 1 HD",
        canonical_name="Rai 1",
        quality_score=300,
        tvg_id="rai1.it",
        url="1",
        extinf=""
    ),

    Channel(
        name="Rai 1 FHD",
        canonical_name="Rai 1",
        quality_score=400,
        tvg_id="rai1.it",
        url="2",
        extinf=""
    ),

    Channel(
        name="Canale 5",
        canonical_name="Canale 5",
        quality_score=300,
        tvg_id="canale5.it",
        url="3",
        extinf=""
    )

]

best, dup = select_best(channels)

assert len(best) == 2

assert len(dup) == 1

assert best[0].quality_score == 400

print("Selector OK")