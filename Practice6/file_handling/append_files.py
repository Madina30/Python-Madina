
# Append new lines to a file

with open("Practice6/file_handling/example.txt", "a", encoding="utf-8") as file:
    file.write("\nThis is a new line.")
    file.write("\nI am learning Python.")

print("New lines added successfully!")

# Read the updated file
with open("Practice6/file_handling/example.txt", "r", encoding="utf-8") as file:
    print(file.read())
