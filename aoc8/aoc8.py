#!/usr/bin/env python3
import math
import sys
import typing

PART2 = True

class Bits:
    __slots__ = ('value',)

    @staticmethod
    def from_letters(letters: str) -> 'Bits':
        value = 0
        for letter in letters:
            segment = ord(letter) - ord('a')
            value |= 1 << segment
        return Bits(value)

    def __init__(self, value: int) -> None:
        self.value = value

    def __xor__(self, other: 'Bits') -> 'Bits':
        return Bits(self.value ^ other.value)

    def __and__(self, other: 'Bits') -> 'Bits':
        return Bits(self.value & other.value)

    def __or__(self, other: 'Bits') -> 'Bits':
        return Bits(self.value | other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: 'Bits') -> bool:
        return self.value == other.value

    def __nonzero__(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return f'{self.value:07b}'

    def __len__(self) -> int:
        return sum(1 for i in range(7) if self.value & (1 << i))

    def log2(self) -> int:
        return int(math.log(self.value) / math.log(2))

INPUT_DIGITS = [
    Bits.from_letters('abcefg'),
    Bits.from_letters('cf'),
    Bits.from_letters('acdeg'),
    Bits.from_letters('acdfg'),
    Bits.from_letters('bcdf'),
    Bits.from_letters('abdfg'),
    Bits.from_letters('abdefg'),
    Bits.from_letters('acf'),
    Bits.from_letters('abcdefg'),
    Bits.from_letters('abcdfg')
]

def solve(patterns: typing.List[Bits]) -> typing.Dict[Bits, Bits]:
    """
    Given all ten patterns of a display, calculate the mapping from the input to the scrambled output. e.g. a Bit.from_letters('a') => Bit.from_letters('c') means segment a should have lit up, but segment c actually did (and hence to unscramble you must go from c to a).
    """
    by_len = {}
    for pattern in patterns:
        try:
            by_len[len(pattern)].append(pattern)
        except KeyError:
            by_len[len(pattern)] = [pattern]

    assert {k: len(v) for k, v in by_len.items()} == {2: 1, 3: 1, 4: 1, 5: 3, 6: 3, 7: 1}

    # These are easy, we only have one of each length
    cf = by_len[2][0]
    acf = by_len[3][0]
    bcdf = by_len[4][0]

    # Step 1
    a = acf ^ cf
    assert len(a) == 1

    # Step 2
    bd = bcdf ^ cf
    assert len(bd) == 2

    # Step 3
    found = [o for o in by_len[6] if o & (a | bcdf) == (a | bcdf)]
    assert len(found) == 1
    abcdfg = found[0]
    g = abcdfg ^ a ^ bcdf
    assert len(g) == 1

    # Step 4
    found = [o for o in by_len[5] if o & (a | bd) == (a | bd)]
    assert len(found) == 1
    abdfg = found[0]
    f = abdfg ^ a ^ bd ^ g
    c = cf ^ f
    assert len(f) == 1 and len(c) == 1

    # Step 5
    found = [o for o in by_len[5] if o != abdfg]
    assert len(found) == 2
    if found[0] & f:
        acdfg, acdeg = found
    else:
        acdeg, acdfg = found

    acdg = acdfg ^ f
    e = acdeg ^ acdg
    assert len(e) == 1

    # Step 6
    found = [o for o in by_len[6] if o & (a | bcdf) != (a | bcdf) and o & c]
    assert len(found) == 1
    abcefg = found[0]

    bc = abcefg ^ a ^ e ^ f ^ g
    b = bc ^ c
    d = bd ^ b
    assert len(b) == 1 and len(d) == 1

    return {Bits(1 << i): x for i, x in enumerate((a, b, c, d, e, f, g))}

def unscramble(scrambled: Bits, mapping: typing.Dict[Bits, Bits]) -> Bits:
    unscrambled = Bits(0)
    for good, bad in mapping.items():
        if scrambled & bad:
            unscrambled |= good
    return unscrambled

def bits_to_digit(unscrambled: Bits) -> int:
    for i, digit in enumerate(INPUT_DIGITS):
        if digit == unscrambled:
            return i
    raise RuntimeError('No matching digit!')

def main() -> None:
    result = 0

    for line in sys.stdin:
        patterns, outputs = line.split('|')
        patterns = [Bits.from_letters(token) for token in patterns.split()]
        outputs = [Bits.from_letters(token) for token in outputs.split()]
        mapping = solve(patterns)
        digits = [bits_to_digit(unscramble(output, mapping)) for output in outputs]
        if PART2:
            result += digits[0] * 1000 + digits[1] * 100 + digits[2] * 10 + digits[3]
        else:
            result += sum(1 for o in digits if o in (1, 4, 7, 8))

    print(result)

if __name__ == '__main__':
    main()
