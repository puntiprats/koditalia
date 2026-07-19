from collections import defaultdict
from models import Channel
from checker import check_stream


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

        if len(group) > 1:

            alive = []

            for channel in group:

                status = check_stream(channel.url)

                channel.alive = status.alive
                channel.response_time = status.response_time
                channel.status_code = status.status_code

                if status.alive:
                    alive.append(channel)

            if alive:
                group = alive

        group.sort(
            key=ranking,
            reverse=True
        )

        selected.append(group[0])

        duplicates.extend(group[1:])

    return selected, duplicates