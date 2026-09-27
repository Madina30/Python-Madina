#1
def squares(N):
    for i in range(N+1):
        yield i*i


N = 10

for number in squares (N):
    print(number)

#2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


n = 20

print(",".join(str(number) for number in even_numbers(n)))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


n =30

for number in divisible_by_3_and_4(n):
    print(number)


#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = 6
b = 9

for value in squares(a, b):
    print(value)


#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


n = 7

for number in countdown(n):
    print(number)