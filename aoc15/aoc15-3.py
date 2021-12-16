#!/usr/bin/env python3
import sys
import typing
from heapq import heappop, heappush
from dataclasses import dataclass

PART2 = True

@dataclass
class Loc:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __lt__(self, other: 'Loc') -> bool:
        if self.row < other.row:
            return True
        if self.row > other.row:
            return False
        return self.col < other.col

class Map:
    @staticmethod
    def from_io(reader: typing.TextIO) -> 'Map':
        costs: list[list[int]] = []
        for line in reader:
            row = [int(token) for token in line.strip()]
            if costs:
                assert len(row) == len(costs[0])
            costs.append(row)
        return Map(costs)

    def __init__(self, costs: list[list[int]]) -> None:
        self._costs = costs

    def expand(self) -> 'Map':
        mirror_count = 5

        out_costs = []
        for i in range(self.rows * mirror_count):
            out_costs.append([0] * (self.columns * mirror_count))

        for mirror_row in range(mirror_count):
            for mirror_col in range(mirror_count):
                for row in range(self.rows):
                    for col in range(self.columns):
                        new_cost = self._costs[row][col] + mirror_row + mirror_col
                        while new_cost > 9:
                            new_cost -= 9
                        out_costs[mirror_row * self.rows + row][mirror_col * self.columns + col] = new_cost

        return Map(out_costs)

    @property
    def rows(self) -> int:
        return len(self._costs)

    @property
    def columns(self) -> int:
        return len(self._costs[0])

    @property
    def source(self) -> Loc:
        return Loc(row=0, col=0)

    @property
    def target(self) -> Loc:
        return Loc(row=self.rows - 1, col=self.columns - 1)

    def __getitem__(self, loc: Loc) -> int:
        if loc.row < 0 or loc.row >= self.rows:
            return sys.maxsize
        if loc.col < 0 or loc.col >= self.columns:
            return sys.maxsize
        return self._costs[loc.row][loc.col]

def h(source: Loc, target: Loc) -> int:
    return abs(source.row - target.row) + abs(source.col - target.col)

def reconstruct_path(came_from: dict[Loc, Loc], map: Map, current: Loc):
    path = [current]
    cost = map[current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
        cost += map[current]
    cost -= map[current] # Exclude first cost
    return path, cost

def main():
    map = Map.from_io(sys.stdin)

    if PART2:
        map = map.expand()

    open_set = [map.source]

    came_from: dict[Loc, Loc] = {}

    g_score: dict[Loc, int] = {}
    g_score[map.source] = 0

    f_score: dict[Loc, int] = {}
    f_score[map.source] = h(map.source, map.target)

    min_heur = sys.maxsize

    while open_set:
        current = heappop(open_set)
        if current == map.target:
            path, cost = reconstruct_path(came_from, map, current)
            print(f'path = {path!r}, cost = {cost!r}')
            return

        for (off_row, off_col) in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
            next = Loc(current.row + off_row, current.col + off_col)
            tentative_g_score = g_score.get(current, sys.maxsize) + map[next]
            if tentative_g_score < g_score.get(next, sys.maxsize):
                came_from[next] = current
                g_score[next] = tentative_g_score
                heur = h(next, map.target)
                f_score[next] = tentative_g_score + heur
                if next not in open_set:
                    heappush(open_set, next)
                if heur < min_heur:
                    print(f'heur = {heur}')
                    min_heur = heur

    raise RuntimeError('target not reached')

if __name__ == '__main__':
    main()
