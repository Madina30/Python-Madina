#1
def my_function(name, age):
  print("My name is", name)
  print("I am" , age + "years old")

my_function(age = "22", name = "Madina")


#2
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

my_function("cat", name = "Katie", age = 3)

#3
def my_function(x, y):
  return x + y

result = my_function(8, 9)
print(result)

#4
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])
