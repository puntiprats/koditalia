from checker import check_stream

TESTS = [
    "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
    "https://example.com/notfound.m3u8",
]

for url in TESTS:

    result = check_stream(url)

    print()
    print(url)
    print(result)