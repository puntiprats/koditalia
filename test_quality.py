from models import Channel
from quality import calculate_quality


def make(name):

    return Channel(
        name=name,
        url="http://test",
        extinf=name
    )


assert calculate_quality(make("Rai 1 UHD")) == 500
assert calculate_quality(make("Rai 1 4K")) == 500
assert calculate_quality(make("Rai 1 FHD")) == 400
assert calculate_quality(make("Rai 1 HD")) == 300
assert calculate_quality(make("Rai 1 SD")) == 100

print("Quality OK")