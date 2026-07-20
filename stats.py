from collections import Counter


def print_sources(channels):

    counter = Counter()

    for c in channels:

        counter[c.source] += 1

    print()

    print("===== SOURCES =====")

    for name, total in sorted(counter.items()):

        print(f"{name:<20} {total}")


def print_selected(selected):

    from collections import Counter

    counter = Counter(
        c.source
        for c in selected
    )

    print()

    print("===== SELECTED =====")

    for name, total in sorted(counter.items()):

        print(f"{name:<20} {total}")