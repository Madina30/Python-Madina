
import shutil
import os

source = "Practice6/file_handling/example.txt"
backup = "Practice6/file_handling/backup.txt"

# Check whether the source file exists
if os.path.isfile(source):
    shutil.copy2(source, backup)
    print("Backup created successfully!")
else:
    print("Source file does not exist.")


# Delete the backup file safely

if os.path.isfile(backup) and os.access(backup, os.W_OK):
    os.remove(backup)
    print("Backup file deleted.")
else:
    print("File does not exist or is not writable.")
