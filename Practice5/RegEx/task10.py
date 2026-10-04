import re

text = "HelloWorld"

result = re.sub(
    r"(?<!^)(?=[A-Z])",
    "_",
    text
).lower()

print(result)