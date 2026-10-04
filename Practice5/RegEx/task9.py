import re

text = "Hello World Python"
result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)

print(result)