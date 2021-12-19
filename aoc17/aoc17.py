#!/usr/bin/env python3
import sys
import re
import typing
from dataclasses import dataclass, replace

# t=x is *before* step x
# t=x + 1 is *after* step x + 1
# position x:
#   px(0) = 0
#   px(t) = px(t - 1) + vx(t)
# position y:
#   py(0) = 0
#   py(t) = py(t - 1) + vy(t)
# velocity x:
#   vx(0) = (user chosen)
#   vx(t) = vx(t - 1) - vx(t - 1) / abs(vx(t - 1))
# velocity y:
#   vy(0) = (user chosen)
#   vy(t) = vy(0) - t

@dataclass
class Position:
    x: int
    y: int

@dataclass
class Velocity:
    x: int
    y: int

class State:
    position: Position
    velocity: Velocity

    def __init__(self, velocity: Velocity) -> None:
        self.position = Position(0, 0)
        self.velocity = replace(velocity)

    def step(self) -> None:
        # The probe's x position increases by its x velocity.
        # The probe's y position increases by its y velocity.
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if
        # it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
        if self.velocity.x > 0:
            self.velocity.x -= 1
        elif self.velocity.x < 0:
            self.velocity.x += 1

        # Due to gravity, the probe's y velocity decreases by 1.
        self.velocity.y -= 1

@dataclass
class BoundingBox:
    min: Position
    max: Position

    def contains(self, other: Position) -> bool:
        return self.min.x <= other.x <= self.max.x and self.min.y <= other.y <= self.max.y

    def classify(self, other: Position) -> typing.Tuple[int, int]:
        x_cmp = 0
        if other.x < self.min.x:
            x_cmp = -1
        elif other.x > self.max.x:
            x_cmp = 1

        y_cmp = 0
        if other.y < self.min.y:
            y_cmp = -1

        elif other.y > self.max.y:
            y_cmp = 1

        return (x_cmp, y_cmp)

def find_min_vel_x(min_px: int) -> int:
    vx = 1
    while True:
        final_px = vx * (vx + 1) / 2
        if final_px >= min_px:
            return vx
        vx += 1

def main():
    match = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$', sys.stdin.readline())
    assert match is not None

    min_pos = Position(x = int(match.group(1)), y = int(match.group(3)))
    max_pos = Position(x = int(match.group(2)), y = int(match.group(4)))
    bbox = BoundingBox(min_pos, max_pos)

    # min_pos must be less than max_pos
    assert min_pos.x < max_pos.x
    assert min_pos.y < max_pos.y

    # target area must be right of starting point
    assert min_pos.x > 0

    # we want to get to get the target window x-wise as slow as possible so we can set vy as high a possible
    min_vel_x = find_min_vel_x(min_pos.x)

    # loop and try things...
    velocity = Velocity(min_vel_x, 0)
    while True:
        state = State(velocity)
        max_y = -10000

        for step in range(sys.maxsize):
            max_y = max(max_y, state.position.y)

            cmp = bbox.classify(state.position)

            if cmp == (0, 0):
                print(f'{velocity} | {step} | found solution, max_y={max_y}')
                velocity.y += 1
                break
            elif cmp == (-1, 0) or cmp == (-1, 1) or cmp == (0, 1):
                # print(f'{velocity} | {step} | still good')
                pass
            else:
                print(f'{velocity} | {step} | in quadrant ({cmp[0]}, {cmp[1]})')
                if cmp != (0, -1):
                    return

            state.step()

if __name__ == '__main__':
    main()
