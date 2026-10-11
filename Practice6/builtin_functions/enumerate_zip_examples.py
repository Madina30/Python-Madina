
# 1. enumerate() - get index and value

fruits = ["apple", "banana", "orange"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

# 2. zip() - combine two lists

names = ["Ali", "Sara", "Madina"]
scores = [90, 85, 95]

for name, score in zip(names, scores):
    print(name, score)

# 3. sorted() - sort a list

numbers = [5, 2, 8, 1, 3]
print("Sorted:", sorted(numbers))
print("Descending:", sorted(numbers, reverse=True))

# 4. len(), sum(), min(), max()

print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
