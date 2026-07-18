from collections import defaultdict

from models import Channel


def select_best(
    channels: list[Channel]
) -> tuple[list[Channel], list[Channel]]:

    groups = defaultdict(list)

    for channel in channels:

        key = channel.identity.lower().strip()

        groups[key].append(channel)

    selected = []
    duplicates = []

    for group in groups.values():

        from ranking import ranking

        group.sort(
            key=ranking,
            reverse=True
        )
        
        selected.append(group[0])

        duplicates.extend(group[1:])

    return selected, duplicates