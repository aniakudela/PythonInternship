import numpy
import time

result = 0


def testAdjacentDigits(number):
    adjacent_groups = 0
    previous_char = 'a'
    in_group = False
    for c in str(number):
        if previous_char == c:
            if not in_group:
                adjacent_groups += 1
            in_group = True
        else:
            in_group = False
        previous_char = c
    return adjacent_groups


def testDigitsDecrease(number):
    last_digit = '0'
    for c in str(number):
        if c < last_digit:
            return False
        last_digit = c
    return True


def f(j):
    return testDigitsDecrease(j) and testAdjacentDigits(j) >= 2


start_time = time.time()
for i in range(372**2, 809**2 + 1):
    if testDigitsDecrease(i) and testAdjacentDigits(i) >= 2:
        result += 1

print('Result: ', result)
print(time.time() - start_time)

# using numpy
start_time = time.time()
rang = numpy.arange(372 ** 2, 809 ** 2 + 1)
vector = numpy.vectorize(f)
result_2 = (vector(rang)).sum()
print(result_2)
print(time.time() - start_time)

