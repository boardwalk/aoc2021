#!/usr/bin/env python3
import sys

data = [int(ln) for ln in sys.stdin]

num_larger = 0
for i in range(len(data) - 1):
    if data[i + 1] > data[i]:
        num_larger += 1

print(num_larger)
