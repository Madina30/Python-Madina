import re

text = "asb"

pattern = r"^a.*b$"

if re.match(pattern, text):
    print("Match")
else:
    print("No match")