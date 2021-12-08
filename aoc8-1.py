#!/usr/bin/env python3
import sys
import typing
from pprint import pprint
from dataclasses import dataclass

DIGITS = [
    {'a', 'b', 'c',      'e', 'f', 'g'}, # 0 [6]
    {          'c',           'f'     }, # 1 [2]
    {'a',      'c', 'd', 'e',      'g'}, # 2 [5]
    {'a',      'c', 'd',      'f', 'g'}, # 3 [5]
    {     'b', 'c', 'd',      'f'     }, # 4 [4]
    {'a', 'b',      'd',      'f', 'g'}, # 5 [5]
    {'a', 'b',      'd', 'e', 'f', 'g'}, # 6 [6]
    {'a',      'c',           'f'     }, # 7 [3]
    {'a', 'b', 'c', 'd', 'e', 'f', 'g'}, # 8 [7]
    {'a', 'b', 'c', 'd',      'f', 'g'}  # 9 [6]
]

@dataclass
class Case:
    patterns: typing.List[str]
    output: typing.List[str]

def read_case(ln: str) -> Case:
    patterns, output = ln.split('|')

    def parse

    return Case(patterns.split(), output.split())

def reduce(patterns: typing.List[str], connections: typing.Dict[str, typing.Set[str]]) -> bool:
    # 1. this segment is only used in these digits
    # 2. this segment is only *unused* in these digits
    


    return False

def solve_case(case: Case) -> None:
    connections = {}

    for c in 'abcdefg':
        connections[c] = set('abcdefg')

    while reduce(case.patterns, connections):
        pass

    pprint(connections)

def main():
    cases = [read_case(ln) for ln in sys.stdin]

    for case in cases:
        solve_case(case)
        if True:
            break

if __name__ == '__main__':
    main()
