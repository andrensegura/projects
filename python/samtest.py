#! /usr/bin/python


def digit_sum(n):
    sum = 0
    for number in str(n):
        sum += int(number)
    return sum
print digit_sum(12345)



