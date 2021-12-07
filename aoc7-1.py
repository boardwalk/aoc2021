#!/usr/bin/env python3
import sys

PART2 = True

if PART2:
    memo = [0]
    def calc_cost(delta):
        while delta >= len(memo):
            memo.append(memo[-1] + len(memo))
        return memo[delta]
else:
    def calc_cost(delta):
        return delta

def main():
    all_horz = [int(token) for token in sys.stdin.readline().strip().split(',')]

    best_cost = sys.maxsize
    best_target = 0

    for target in range(min(all_horz), max(all_horz) + 1):
        cost = sum(calc_cost(abs(target - horz)) for horz in all_horz)
        if cost < best_cost:
            best_cost = cost
            best_target = target

    print(f'best cost: {best_cost} target: {best_target}')

if __name__ == '__main__':
    main()
