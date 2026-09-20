#1
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Good morning", "Malika", "Nazerke", "Madina")

#2
def my_function(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num

print(my_function(4, 8, 5, 9, 10))

#3
def my_function(fname, lname):
  print("Hello", fname, lname)

person = {"fname": "Aelita", "lname": "Redfhv"}
my_function(**person)

#4
def my_function(a, b, c):
  return a + b + c

numbers = [9, 7, 8]
result = my_function(*numbers)
print(result)
