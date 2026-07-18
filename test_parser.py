from parser import parse_extinf


line = '#EXTINF:-1 tvg-id="rai1.it" tvg-name="Rai 1" group-title="Rai",Rai 1 HD'

attrs, name = parse_extinf(line)

assert name == "Rai 1 HD"
assert attrs["tvg-id"] == "rai1.it"
assert attrs["tvg-name"] == "Rai 1"

print("Parser OK")