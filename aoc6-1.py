#!/usr/bin/env python3
import sys
import typing

def step(fishies: typing.List[int]) -> None:
    for i in range(len(fishies)):
        age = fishies[i]
        if age > 0:
            # just get older
            fishies[i] -= 1
        else:
            # time to reset and spawn another fish
            fishies[i] = 6
            fishies.append(8)

def main():
    fishies = [int(token) for token in sys.stdin.readline().strip().split(',')]
    for day in range(256):
        step(fishies)
        print(f'On day {day + 1} there are {len(fishies)} lanternfish')

if __name__ == '__main__':
    main()
