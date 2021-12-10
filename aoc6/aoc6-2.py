#!/usr/bin/env python3
import sys
import typing

def step(fishies: typing.List[int]) -> None:
    # rotate list: index 0 becomes index 8 (everything gets 'older')
    fishies[:] = fishies[1:] + fishies[:1]

    # everything at index 0 spawned a new fish (already at 8)
    # but we need to also move the index 0 fish to index 6
    fishies[6] += fishies[8]

def main():
    fishies = [0] * 9

    for token in sys.stdin.readline().strip().split(','):
        age = int(token)
        fishies[age] += 1

    for day in range(256):
        step(fishies)
        all_fishies = sum(count for count in fishies)
        print(f'On day {day + 1} there are {all_fishies} lanternfish')

if __name__ == '__main__':
    main()
