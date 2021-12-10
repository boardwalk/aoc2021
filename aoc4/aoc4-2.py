#!/usr/bin/env python3
import sys
import typing
from dataclasses import dataclass

T = typing.TypeVar('T')

class Grid(typing.Generic[T]):
    def __init__(self, default_value: T) -> None:
        self.values = [default_value] * 25

    def __getitem__(self, key: typing.Tuple[int, int]) -> T:
        assert key[0] in range(5) and key[1] in range(5)
        return self.values[key[0] * 5 + key[1]]

    def __setitem__(self, key: typing.Tuple[int, int], value: T) -> None:
        assert key[0] in range(5) and key[1] in range(5)
        self.values[key[0] * 5 + key[1]] = value

class Board(Grid[int]):
    def __init__(self) -> None:
        super().__init__(0)

class Marking(Grid[int]):
    def __init__(self) -> None:
        super().__init__(False)

@dataclass
class BoardState:
    board: Board
    marking: Marking
    won: bool

def read_input(input: typing.TextIO) -> typing.Tuple[list[int], list[Board]]:
    numbers = [int(num) for num in input.readline().split(',')]
    boards: list[Board] = []
    row = 0
    for line in input:
        line = line.strip()
        if line:
            tokens = line.split()
            assert len(tokens) == 5
            for col, token in enumerate(tokens):
                boards[-1][row, col] = int(token)
            row += 1
        else:
            if boards:
                assert row == 5
                row = 0
            boards.append(Board())
    assert row == 5
    return numbers, boards

def mark_board(board: Board, marking: Marking, number: int) -> bool:
    marked = False
    for row in range(5):
        for col in range(5):
            if board[row, col] == number:
                marking[row, col] = True
                marked = True
    return marked

def marking_wins(marking: Marking) -> bool:
    if any(all(marking[row, col] for col in range(5)) for row in range(5)):
        return True
    if any(all(marking[row, col] for row in range(5)) for col in range(5)):
        return True
    return False

def score_board(board: Board, marking: Marking, number: int) -> int:
    score = 0
    for row in range(5):
        for col in range(5):
            if not marking[row, col]:
                score += board[row, col]
    return score * number

def main():
    numbers, boards = read_input(sys.stdin)
    board_states = [BoardState(board, Marking(), won=False) for board in boards]
    for number in numbers:
        print(f'calling {number}')
        for b, state in enumerate(board_states):
            if state.won:
                continue
            if mark_board(state.board, state.marking, number) and marking_wins(state.marking):
                score = score_board(state.board, state.marking, number)
                print(f'board {b} won with score {score}')
                state.won = True
        if all(state.won for state in board_states):
            break

if __name__ == '__main__':
    main()
