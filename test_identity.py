from identity import build_identity

assert build_identity("Rai 1 HD") == "Rai 1"

assert build_identity("Rai1.it@HD") == "Rai 1"

assert build_identity("Rai1.it@SD") == "Rai 1"

assert build_identity("Canale5 HD") == "Canale 5"

print("Identity OK")