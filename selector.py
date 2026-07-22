from collections import defaultdict

from models import Channel
from ranking import ranking
from checker import check_streams


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

        if len(group) > 1 and len({c.url for c in group}) > 1:
            check_streams(group)

            alive = [
                channel
                for channel in group
                if channel.alive and not channel.geo_blocked
            ]

            if alive:
                group = alive

        group.sort(
            key=ranking,
            reverse=True
        )

        group[0].selected_reason = (
            f"{group[0].source} "
            f"(quality={group[0].quality_score}, "
            f"response={group[0].response_time})"
        )

        selected.append(group[0])

        duplicates.extend(group[1:])

    return selected, duplicates