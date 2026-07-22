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

            print(
                f"\n===== GROUP {group[0].identity} ====="
            )

            for channel in group:

                print(
                    channel.name,
                    "| source:",
                    channel.source,
                    "| url:",
                    channel.url,
                    "| alive:",
                    channel.alive,
                    "| geo:",
                    channel.geo_blocked,
                    "| status:",
                    channel.status_code,
                    "| quality:",
                    channel.quality_score,
                )



            for channel in group:

                if channel.identity in (
                    "Rai 1",
                    "Rai 3",
                ):
                    print(
                        channel.identity,
                        "|",
                        channel.url,
                        "| alive:",
                        channel.alive,
                        "| quality:",
                        channel.quality_score,
                        "| response:",
                        channel.response_time,
                        "| status:",
                        channel.status_code,
                    )


            for channel in group:

                if channel.alive and not channel.geo_blocked:
                    alive.append(channel)

            if alive:
                group = alive


            print("\nRANK DEBUG:", group[0].identity)

            for c in group:
                print(
                    c.source,
                    "|",
                    c.url,
                    "| alive:",
                    c.alive,
                    "| geo:",
                    c.geo_blocked,
                    "| quality:",
                    c.quality_score,
                    "| priority:",
                    c.source_priority,
                    "| rank:",
                    ranking(c)
                )


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