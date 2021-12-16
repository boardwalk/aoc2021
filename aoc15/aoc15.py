#!/usr/bin/env python3
import sys

def get_cost(costs, row, col):
    if row < 0 or col < 0:
        return sys.maxsize
    if row >= len(costs) or col >= len(costs[0]):
        return sys.maxsize
    return costs[row][col]

def main():
    grid = []
    costs = []
    for line in sys.stdin:
        row = [int(token) for token in line.strip()]
        grid.append(row)
        costs.append([None] * len(row))

    width = len(grid[0])
    height = len(grid)

    print(grid)
    print(costs)
    print(width)
    print(height)

    # it costs 0 to get to the top left
    costs[0][0] = 0

    # we want to calculate the bottom right
    stack = [ (height - 1, width - 1) ]

    while stack:
        print(f'stack size = {len(stack)}')
        r, c = stack[-1]

        if costs[r][c] is not None:
            stack.pop()
            continue

        missing = False
        if get_cost(costs, r - 1, c) is None:
            stack.append((r - 1, c))
            missing = True
        if get_cost(costs, r + 1, c) is None:
            stack.append((r + 1, c))
            missing = True
        if get_cost(costs, r, c - 1) is None:
            stack.append((r, c - 1))
            missing = True
        if get_cost(costs, r, c + 1) is None:
            stack.append((r, c + 1))
            missing = True

        if missing:
            continue

        costs[r][c] = min(get_cost(costs, r - 1, c),
            get_cost(costs, r + 1, c),
            get_cost(costs, r, c - 1),
            get_cost(costs, r, c + 1)) + grid[r][c]
        stack.pop()

    print(costs)
    # print( calc_cost(grid, costs, height - 1, width - 1) )

    # queue = []
    # queue.append( (height - 1, width - 1) )

    # while queue:
    #     next_pos = queue.pop()

if __name__ == '__main__':
    main()
