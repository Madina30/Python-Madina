#1

import os

path = "Practice6"

print("Directories:")
print(os.listdir(path))

print("\nOnly directories:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isdir(full_path):
        print(item)

print("\nOnly files:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isfile(full_path):
        print(item)

#2

import os

path = "Practice6"

print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))



# Task 3: Check a path and get its filename and directory

import os

path = "Practice6/file_handling/example.txt"

if os.path.exists(path):
    print("Path exists")
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(path))
else:
    print("Path does not exist")



# Task 4: Count the number of lines

path = "Practice6/file_handling/example.txt"

with open(path, "r", encoding="utf-8") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))



# Task 5: Write a list to a file

items = ["Apple", "Banana", "Orange", "Mango"]

path = "Practice6/file_handling/list.txt"

with open(path, "w", encoding="utf-8") as file:
    for item in items:
        file.write(item + "\n")

print("List written to file successfully!")


# Task 6: Create 26 text files from A.txt to Z.txt

import os
import string

folder = "Practice6/file_handling/letters"
os.makedirs(folder, exist_ok=True)

for letter in string.ascii_uppercase:
    path = os.path.join(folder, letter + ".txt")

    with open(path, "w", encoding="utf-8") as file:
        file.write("This is file " + letter)

print("26 files created successfully!")


# Task 7: Copy the contents of a file to another file

source = "Practice6/file_handling/example.txt"
destination = "Practice6/file_handling/copied_content.txt"

with open(source, "r", encoding="utf-8") as source_file:
    content = source_file.read()

with open(destination, "w", encoding="utf-8") as destination_file:
    destination_file.write(content)

print("File contents copied successfully!")


# Task 8: Delete a file safely

import os

path = input("Enter the file path to delete: ")

if not os.path.exists(path):
    print("Error: The path does not exist.")
elif not os.path.isfile(path):
    print("Error: The path is not a file.")
elif not os.access(path, os.W_OK):
    print("Error: No write permission.")
else:
    confirm = input("Are you sure you want to delete this file? (yes/no): ")

    if confirm.lower() == "yes":
        try:
            os.remove(path)
            print("File deleted successfully.")
        except OSError as error:
            print("Could not delete the file:", error)
    else:
        print("Deletion cancelled.")

