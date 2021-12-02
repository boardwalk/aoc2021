#!/usr/bin/env python3
import re
import sys

horz = 0
depth = 0
for ln in sys.stdin:
    m = re.match(r'(forward|down|up) (\d+)$', ln)
    assert m is not None
    val = int(m.group(2))
    if m.group(1) == 'forward':
        horz += val
    elif m.group(1) == 'down':
        depth += val
    elif m.group(1) == 'up':
        depth -= val

print(horz * depth)
