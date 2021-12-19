#!/usr/bin/env python3
import sys
from pprint import pprint
from copy import deepcopy

PART2 = True

class TextReader:
    def __init__(self, s):
        self.s = s
        self.pos = 0

    def peek(self):
        return self.s[self.pos]

    def read(self):
        c = self.s[self.pos]
        self.pos += 1
        return c

    def __len__(self):
        return len(self.s) - self.pos

def parse_number_pair(rd):
    assert rd.read() == '['
    first = parse_number(rd)
    assert rd.read() == ','
    second = parse_number(rd)
    assert rd.read() == ']'
    return [first, second]

def parse_number_literal(rd):
    val = 0
    while rd.peek().isdigit():
        val = val * 10 + (ord(rd.read()) - ord('0'))
    return val

def parse_number(rd):
    if rd.peek() == '[':
        return parse_number_pair(rd)
    elif rd.peek().isdigit():
        return parse_number_literal(rd)
    else:
        raise RuntimeError('unexpected character in number')

def find_exploder(num, *, depth=0):
    # print(f'find_exploder({num}, depth={depth})')
    if isinstance(num, list):
        if depth >= 4 and isinstance(num[0], int) and isinstance(num[1], int):
            return []

        left = find_exploder(num[0], depth=depth + 1)
        if left is not None:
            return [0] + left

        right = find_exploder(num[1], depth=depth + 1)
        if right is not None:
            return [1] + right

    return None

def find_splitter(num):
    if isinstance(num, list):
        left = find_splitter(num[0])
        if left is not None:
            return [0] + left
        right = find_splitter(num[1])
        if right is not None:
            return [1] + right
    elif isinstance(num, int):
        if num >= 10:
            return []
    else:
        raise RuntimeError('unexpected value inside number')
    return None

def find_literals_inner(num, *, path, result):
    if isinstance(num, list):
        find_literals_inner(num[0], path=path + [0], result=result)
        find_literals_inner(num[1], path=path + [1], result=result)
    elif isinstance(num, int):
        result.append(path)
    else:
        raise RuntimeError('unexpected value inside number')

def find_literals(num):
    result = []
    find_literals_inner(num, path=[], result=result)
    return result

def left_lit(num, path):
    left_path = None
    for lit in find_literals(num):
        if lit < path:
            left_path = lit
    return left_path

def right_lit(num, path):
    right_path = None
    for lit in reversed(find_literals(num)):
        if lit > path:
            right_path = lit
    return right_path

def get(num, path):
    for idx in path:
        num = num[idx]
    return num

def set(num, path, val):
    for idx in path[:-1]:
        num = num[idx]
    num[path[-1]] = val

def reduce(num):
    while True:
        # print(f'num is {num}')

        exploder_path = find_exploder(num)
        if exploder_path is not None:
            left_path = left_lit(num, exploder_path + [0])
            right_path = right_lit(num, exploder_path + [1])

            # print(f'found exploder at {exploder_path} ({get(num, exploder_path)})')

            if left_path is not None:
                # print(f'left literal is {left_path} ({get(num, left_path)})')
                set(num, left_path, get(num, left_path) + get(num, exploder_path + [0]))
            if right_path is not None:
                # print(f'right literal is {right_path} ({get(num, right_path)})')
                set(num, right_path, get(num, right_path) + get(num, exploder_path + [1]))

            set(num, exploder_path, 0)
            continue

        splitter_path = find_splitter(num)
        if splitter_path is not None:
            # print(f'found splitter at {splitter_path} ({get(num, splitter_path)})')

            val = get(num, splitter_path)
            val_left = int(val / 2)
            val_right = int(val / 2 + 0.5)
            # print(f'replacing {val} with ({val_left}, {val_right})')
            set(num, splitter_path, [val_left, val_right])
            continue

        break

    return num

def magnitude(num):
    if isinstance(num, list):
        return 3 * magnitude(num[0]) + 2 * magnitude(num[1])
    elif isinstance(num, int):
        return num
    else:
        raise RuntimeError('unexpected value inside number')

def parse_number2(s):
    s = s.strip()
    rd = TextReader(s)
    num = parse_number(rd)
    assert len(rd) == 0
    return num

def main():
    numbers = [parse_number2(ln.strip()) for ln in sys.stdin]
    pprint(numbers)

    if PART2:
        max_mag = 0
        for i, num1 in enumerate(numbers):
            for j, num2 in enumerate(numbers):
                if j <= i:
                    continue
                mag1 = magnitude(reduce(deepcopy([num1, num2])))
                mag2 = magnitude(reduce(deepcopy([num2, num1])))
                # print(f'{num1} + {num2} = {mag1}')
                # print(f'{num2} + {num1} = {mag2}')
                max_mag = max(max_mag, mag1)
                max_mag = max(max_mag, mag2)

        print(f'magnitude: {max_mag}')
    else:
        left = None
        for right in numbers:
            if left is None:
                left = right
            else:
                left = reduce([left, right])

        print(f'result: {left}')
        print(f'magnitude: {magnitude(left)}')

if __name__ == '__main__':
    main()
