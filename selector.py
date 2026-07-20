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

        if len(group) > 1 and len({c.url for c in group}) > 1:

            from checker import check_streams

            alive = []

            check_streams(group)

            for channel in group:

                if channel.alive:
                    alive.append(channel)

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

        for duplicate in group[1:]:

            if (
                duplicate.source == group[0].source
                or not duplicate.alive
            ):
                continue

            print(
                f"{group[0].identity}: "
                f"{group[0].source} > {duplicate.source}"
            )

    return selected, duplicates