from collections import Counter


def print_sources(channels):

    counter = Counter()

    for c in channels:

        counter[c.source] += 1

    print()

    print("===== SOURCES =====")

    for name, total in sorted(counter.items()):

        print(f"{name:<20} {total}")