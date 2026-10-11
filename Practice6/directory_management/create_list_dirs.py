
import os

# 1. Get the current working directory
print("Current directory:")
print(os.getcwd())

# 2. Create nested directories
os.makedirs("Practice6/directory_management/test_folder/documents",
            exist_ok=True)

print("Nested directories created!")

# 3. List all items in the current directory
print("Items in Practice6:")
print(os.listdir("Practice6"))


# 4. List only directories and files

path = "Practice6"

print("\nDirectories:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isdir(full_path):
        print(item)

print("\nFiles:")
for item in os.listdir(path):
    full_path = os.path.join(path, item)
    if os.path.isfile(full_path):
        print(item)


# 5. Find Python files

print("\nPython files:")

for root, dirs, files in os.walk("Practice6"):
    for file in files:
        if file.endswith(".py"):
            print(os.path.join(root, file))
