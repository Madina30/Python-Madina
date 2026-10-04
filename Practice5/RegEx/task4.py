import re

text = "Python"

pattern = r"\b[A-Z][a-z]+\b"

result = re.findall(pattern, text)

print(result)