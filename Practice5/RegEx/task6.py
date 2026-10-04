import re

text = "name type. age"

result = re.sub(r"[ ,.]", ":", text)

print(result)