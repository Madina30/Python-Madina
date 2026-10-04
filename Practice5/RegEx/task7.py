import re

text = "hello_world"
result = re.sub(
    r"_([a-z])",
    lambda x: x.group(1).upper(),
    text
)

print(result)