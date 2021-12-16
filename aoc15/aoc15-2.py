#!/usr/bin/env python3
import sys
import heapq
from dataclasses import dataclass
import typing

PART2 = False

@dataclass
class Loc:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))

@dataclass
class Node:
    loc: Loc
    curr_cost: int
    min_total_cost: int
    parent: typing.Optional['Node']
    dead: bool

    def __lt__(self, other: 'Node') -> bool:
        return self.min_total_cost < other.min_total_cost

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            raise NotImplemented
        return self.min_total_cost == other.min_total_cost

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
                        new_cost = (self._costs[row][col] + mirror_row + mirror_col) % 10
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

class NodeCollection:
    _heap: list[Node]
    _by_loc: dict[Loc, Node]

    def __init__(self) -> None:
        self._heap = []
        self._by_loc = {}

    def pop(self) -> Node:
        while True:
            node = heapq.heappop(self._heap)
            if not node.dead:
                del self._by_loc[node.loc]
                return node

    def insert(self, node: Node) -> None:
        # If the node already exists,
        # and it's cheaper, return, ignoring the new node
        # else, nuke the old node
        try:
            existing_node = self._by_loc[node.loc]
            if existing_node.min_total_cost < node.min_total_cost:
                return
            existing_node.dead = True
            del self._by_loc[node.loc]
        except KeyError:
            pass

        heapq.heappush(self._heap, node)
        self._by_loc[node.loc] = node

def heur(source: Loc, map: Map) -> int:
    return (abs(map.target.row - source.row) + abs(map.target.col - source.col))

def make_neighbor(parent: Node, off_row: int, off_col: int, map: Map) -> Node:
    loc = Loc(parent.loc.row + off_row, parent.loc.col + off_col)
    curr_cost = parent.curr_cost + map[loc]
    min_total_cost = curr_cost + heur(loc, map)
    return Node(loc=loc, curr_cost=curr_cost, min_total_cost=min_total_cost, parent=parent, dead=False)

def main() -> None:
    map = Map.from_io(sys.stdin)

    if PART2:
        map = map.expand()

    nodes = NodeCollection()
    start_node = Node(loc=map.source, curr_cost=0, min_total_cost=heur(map.source, map), parent=None, dead=False)
    nodes.insert(start_node)

    # best_min_total_cost = sys.maxsize

    while True:
        node = nodes.pop()

        if node.loc == map.target:
            break

        # if node.min_total_cost < best_min_total_cost:
        #     best_min_total_cost = node.min_total_cost
        # print(f'saw min_total_cost = {best_min_total_cost}')

        for (off_row, off_col) in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
            nodes.insert(make_neighbor(node, off_row, off_col, map))

    curr: typing.Optional[Node] = node
    path = []
    while curr is not None:
        path.append((curr.loc, curr.curr_cost, curr.min_total_cost))
        curr = curr.parent

    path.reverse()

    from pprint import pprint
    pprint(path)

if __name__ == '__main__':
    main()
