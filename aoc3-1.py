#!/usr/bin/env python3
import sys

num_digits = 0
num_lines = 0
data = []
for ln in sys.stdin:
    ln = ln.strip()
    num_digits = max(num_digits, len(ln))
    data.append(int(ln, 2))
    num_lines += 1

count_ones = {}
for val in data:
    i = 0
    while val != 0:
        if val & 1:
            try:
                count_ones[i] += 1
            except KeyError:
                count_ones[i] = 1
        val >>= 1
        i += 1

gamma = 0
beta = 0
for i in range(num_digits):
    num_ones = count_ones.get(i, 0)
    num_zeros = num_lines - num_ones
    if num_ones > num_zeros:
        gamma = gamma | (1 << i)
    elif num_ones < num_zeros:
        beta = beta | (1 << i)
    else:
        raise RuntimError('equal ones and zeros')

print(gamma * beta)
