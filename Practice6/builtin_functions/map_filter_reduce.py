
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# 1. map() - multiply each number by 2
doubled = list(map(lambda x: x * 2, numbers))
print("Doubled:", doubled)

# 2. filter() - select even numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# 3. reduce() - calculate the sum
total = reduce(lambda x, y: x + y, numbers)
print("Total:", total)
