#!/usr/bin/env python3
import sys
import typing

# read numbers
numbers = [int(num) for num in sys.stdin.readline().split(',')]

# read boards
# stored row major (rows are contiguous)

boards = []
for line in sys.stdin:
    line = line.strip()
    if line:
        row = [int(num) for num in line.split()]
        assert len(row) == 5
        boards[-1].extend(row)
    else:
        if boards:
            assert len(boards[-1]) == 25
        boards.append([])

assert len(boards[-1]) == 25

# evaluate boards

def mark_board(board: list[int], numbers: list[int]) -> list[bool]:
    marked = [False] * 25
    for num in numbers:
        for i, board_num in enumerate(board):
            if board_num == num:
                marked[i] = True
    return marked

def row_all_marked(marked: list[bool], row: int) -> bool:
    return all(marked[row * 5 + col] for col in range(5))

def col_all_marked(marked: list[bool], col: int) -> bool:
    return all(marked[row * 5 + col] for row in range(5))

def board_wins(marked: list[bool]) -> bool:
    if any(row_all_marked(marked, row) for row in range(5)):
        return True
    if any(col_all_marked(marked, col) for col in range(5)):
        return True
    return False

def board_score(board: list[int], marked: list[bool]) -> bool:
    return sum(num for i, num in enumerate(board) if not marked[i])

def eval_board(board: list[int], numbers: list[int]) -> typing.Optional[int]:
    marked = mark_board(board, numbers)
    return board_score(board, marked) * numbers[-1] if board_wins(marked) else None

def eval_boards(boards: list[list[int]], numbers: list[int]) -> typing.Optional[typing.Tuple[int, int]]:
    for i, board in enumerate(boards):
        score = eval_board(board, numbers)
        if score is not None:
            return (i, score)
    return None

found = False

for i in range(1, len(numbers)):
    print(f'eval_boards with numbers: {numbers[0:i]}')
    result = eval_boards(boards, numbers[0:i])
    if result is not None:
        print(f'board {result[0]} won with score {result[1]}')
        found = True
        break

if not found:
    print('nothing won!')
