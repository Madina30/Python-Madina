
import os
import shutil

# Create folders
source_dir = "Practice6/directory_management/source"
copy_dir = "Practice6/directory_management/copies"
move_dir = "Practice6/directory_management/moved"

os.makedirs(source_dir, exist_ok=True)
os.makedirs(copy_dir, exist_ok=True)
os.makedirs(move_dir, exist_ok=True)

# Create a sample file
source_file = os.path.join(source_dir, "example.txt")

with open(source_file, "w", encoding="utf-8") as file:
    file.write("This file is used for Practice 6.")

# Copy the file
copy_file = os.path.join(copy_dir, "example_copy.txt")
shutil.copy2(source_file, copy_file)

print("File copied successfully!")

# Move the original file
moved_file = os.path.join(move_dir, "example.txt")
shutil.move(source_file, moved_file)

print("File moved successfully!")
