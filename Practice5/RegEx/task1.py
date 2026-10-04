#1
import re

text = "abb"
pattern = r"^ab*$"

if re.match(pattern, text):
    print("Match")
else:
    print("No match")
