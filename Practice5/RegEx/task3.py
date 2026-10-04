import re

text = "hello_world"

pattern = r"\b[a-z]+_[a-z]+\b"

result = re.findall(pattern, text)

print(result)