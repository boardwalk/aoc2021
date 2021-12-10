#!/usr/bin/env python3
import re
import sys

PART2 = True

def delta(a, b):
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0

def main():
    # (x, y) => count
    counts = {}

    for ln in sys.stdin:
        ln = ln.strip()
        m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)$', ln)
        assert m is not None

        x1 = int(m.group(1))
        y1 = int(m.group(2))
        x2 = int(m.group(3))
        y2 = int(m.group(4))

        dx = delta(x1, x2)
        dy = delta(y1, y2)

        if dx != 0 and dy != 0:
            if not PART2:
                continue
            assert abs(x1 - x2) == abs(y1 - y2), 'Line not at 0, 45, or 90 degrees'

        if dx != 0:
            dist = abs(x1 - x2)
        elif dy != 0:
            dist = abs(y1 - y2)
        else:
            assert False, 'Line without any length'

        for step in range(dist + 1):
            x = x1 + dx * step
            y = y1 + dy * step
            key = (x, y)
            try:
                counts[key] += 1
            except KeyError:
                counts[key] = 1

    num_intersections = sum(1 for c in counts.values() if c >= 2)
    print(num_intersections)

if __name__ == '__main__':
    main()
