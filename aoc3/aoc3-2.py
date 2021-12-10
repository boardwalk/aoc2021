#!/usr/bin/env python3
import sys

data = [ln.strip() for ln in sys.stdin]
num_cols = len(data[0])

def count_ones(data, col):
    return sum(1 for row in data if row[col] == '1')

def o2_keep_what(num_zero, num_one):
    return '0' if num_zero > num_one else '1'

def co2_keep_what(num_zero, num_one):
    return '0' if num_zero <= num_one else '1'

def find_value(keep_what):
    filtered_data = list(data)
    col = 0

    while True:
        if len(filtered_data) == 0:
            raise RuntimeError('Out of rows')
        if len(filtered_data) == 1:
            return int(filtered_data[0], 2)
        if col >= num_cols:
            raise RuntimeError('Out of cols')

        num_one = count_ones(filtered_data, col)
        num_zero = len(filtered_data) - num_one
        digit = keep_what(num_zero, num_one)
        filtered_data = [row for row in filtered_data if row[col] == digit]

        col += 1

o2_val = find_value(o2_keep_what)
co2_val = find_value(co2_keep_what)
print(o2_val * co2_val)
