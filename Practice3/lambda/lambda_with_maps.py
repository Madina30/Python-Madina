#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 25, numbers))
print(doubled)

#2
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#3
students = [("Emil", 30), ("Tobias", 25), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

