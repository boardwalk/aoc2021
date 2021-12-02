#!/usr/bin/env python3
import sys

data = [int(ln) for ln in sys.stdin]

num_larger = 0
window_size = 3
for i in range(len(data) - window_size):
    first_sum = sum(data[i:i+window_size])
    second_sum = sum(data[i+1:i+window_size+1])
    if second_sum > first_sum:
        num_larger += 1

print(num_larger)
