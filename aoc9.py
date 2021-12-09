#!/usr/bin/env python3
import functools
import sys
import typing

PART2 = True

class Map:
    @staticmethod
    def from_file(f: typing.TextIO) -> 'Map':
        data = []
        rows = 0
        columns = None
        for ln in f:
            len_before = len(data)
            data.extend(int(ch) for ch in ln.strip())
            len_after = len(data)
            this_columns = len_after - len_before
            if columns is None:
                columns = this_columns
            else:
                assert this_columns == columns
            rows += 1
        return Map(data, rows, columns)

    def __init__(self, data: typing.List[int], rows: int, columns: int) -> None:
        self._data = data
        self._rows = rows
        self._columns = columns

    def __getitem__(self, key: typing.Tuple[int, int]) -> int:
        r, c = key
        if r not in range(self._rows) or c not in range(self._columns):
            return sys.maxsize
        return self._data[r * self._columns + c]

    def __setitem__(self, key: typing.Tuple[int, int], value: int) -> None:
        r, c = key
        if r not in range(self._rows) or c not in range(self._columns):
            return
        self._data[r * self._columns + c] = value

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

def main():
    map = Map.from_file(sys.stdin)

    low_points = []
    for r in range(map.rows):
        for c in range(map.columns):
            if (map[r, c] < map[r - 1, c] and map[r, c] < map[r + 1, c] and
                map[r, c] < map[r, c - 1] and map[r, c] < map[r, c + 1]):
                low_points.append((r, c))

    if PART2:
        sizes = []
        for low_point in low_points:
            work_queue = [low_point]
            size = 0
            while work_queue:
                point = work_queue.pop()
                if map[point] >= 9:
                    continue
                map[point] = 9
                size += 1
                work_queue.extend((
                    (point[0] - 1, point[1]),
                    (point[0] + 1, point[1]),
                    (point[0], point[1] - 1),
                    (point[0], point[1] + 1)
                ))
            sizes.append(size)

        sizes.sort(reverse=True)
        sizes = sizes[:3]

        mul_sizes = functools.reduce(int.__mul__, sizes, 1)
        print(mul_sizes)
    else:
        total_risk = 0
        for low_point in low_points:
            risk = 1 + map[low_point]
            print(risk)
            total_risk += risk

        print(total_risk)

if __name__ == '__main__':
    main()
