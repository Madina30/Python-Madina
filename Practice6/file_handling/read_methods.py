
# Method 1: read() - reads the entire file
with open("Practice6/file_handling/example.txt", "r", encoding="utf-8") as file:
    print("READ:")
    print(file.read())

# Method 2: readline() - reads one line
with open("Practice6/file_handling/example.txt", "r", encoding="utf-8") as file:
    print("READLINE:")
    print(file.readline())

# Method 3: readlines() - returns all lines as a list
with open("Practice6/file_handling/example.txt", "r", encoding="utf-8") as file:
    print("READLINES:")
    print(file.readlines())
