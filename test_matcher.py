from matcher import canonical_name


assert canonical_name("RAI UNO HD") == "Rai 1"

assert canonical_name("Rai1") == "Rai 1"

assert canonical_name("Canale5 HD") == "Canale 5"

print("Matcher OK")