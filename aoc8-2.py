#!/usr/bin/env python3
import sys
import math
import typing

PART2 = True

def bitlen(value: int) -> int:
	return sum(1 for i in range(7) if value & (1 << i))

class ConnState:
	__slots__ = ('value',)
	def __init__(self, letters: str) -> None:
		self.value = 0
		for letter in letters:
			segment = ord(letter) - ord('a')
			self.value |= 1 << segment

	def __repr__(self) -> str:
		return f'{self.value:07b}'

INPUT_DIGITS = [
	ConnState('abcefg'), # 0
	ConnState('cf'), # 1
	ConnState('acdeg'), # 2
	ConnState('acdfg'), # 3
	ConnState('bcdf'), # 4
	ConnState('abdfg'), # 5
	ConnState('abdefg'), # 6
	ConnState('acf'), # 7
	ConnState('abcdefg'), # 8
	ConnState('abcdfg') # 9
]

def log2(val: int) -> int:
	return int(math.log(val) / math.log(2))

def solve(outputs: typing.List[ConnState]) -> typing.Dict[int, int]:
	by_len = {}
	for output in outputs:
		try:
			by_len[bitlen(output.value)].append(output)
		except KeyError:
			by_len[bitlen(output.value)] = [output]

	assert len(by_len[2]) == 1
	assert len(by_len[3]) == 1
	assert len(by_len[4]) == 1
	assert len(by_len[5]) == 3
	assert len(by_len[6]) == 3
	assert len(by_len[7]) == 1

	# These are easy we only have one of each length
	cf = by_len[2][0].value
	acf = by_len[3][0].value
	bcdf = by_len[4][0].value

	# Step 1
	a = acf ^ cf
	assert bitlen(a) == 1

	# Step 2
	bd = bcdf ^ cf
	assert bitlen(bd) == 2

	# Step 3
	found = [o.value for o in by_len[6] if o.value & (a | bcdf) == (a | bcdf)]
	assert len(found) == 1
	abcdfg = found[0]
	g = abcdfg ^ a ^ bcdf
	assert bitlen(g) == 1

	# Step 4
	found = [o.value for o in by_len[5] if o.value & (a | bd) == (a | bd)]
	assert len(found) == 1
	abdfg = found[0]
	f = abdfg ^ a ^ bd ^ g
	c = cf ^ f
	assert bitlen(f) == 1
	assert bitlen(c) == 1

	# Step 5
	found = [o.value for o in by_len[5] if o.value != abdfg]
	assert len(found) == 2
	if found[0] & f:
		acdfg, acdeg = found
	else:
		acdeg, acdfg = found

	acdg = acdfg ^ f
	e = acdeg ^ acdg
	assert bitlen(e) == 1

	# Step 6
	found = [o.value for o in by_len[6] if o.value & (a | bcdf) != (a | bcdf)]
	assert len(found) == 2
	if found[0] & c:
		abcefg, abdefg = found
	else:
		abdefg, abcefg = found

	bc = abcefg ^ a ^ e ^ f ^ g
	b = bc ^ c
	d = bd ^ b

	# print(f'a       = {a:07b}')
	# print(f'b       = {b:07b}')
	# print(f'c       = {c:07b}')
	# print(f'd       = {c:07b}')
	# print(f'e       = {e:07b}')
	# print(f'f       = {f:07b}')
	# print(f'g       = {g:07b}')

	return { 
		0: log2(a),
		1: log2(b),
		2: log2(c),
		3: log2(d),
		4: log2(e),
		5: log2(f),
		6: log2(g),
	}

def fix(cs: ConnState, mapping: typing.Dict[int, int]) -> int:
	value = 0
	for new, old in mapping.items():
		if cs.value & (1 << old):
			value |= (1 << new)

	for i, digit in enumerate(INPUT_DIGITS):
		if digit.value == value:
			return i

	raise RuntimeError('No matching digit!')

def main() -> None:
	result = 0

	for line in sys.stdin:
		patterns, output = line.split('|')
		patterns = [ConnState(token) for token in patterns.split()]
		output = [ConnState(token) for token in output.split()]
		mapping = solve(patterns)
		fixed_output = [fix(cs, mapping) for cs in output]
		if PART2:
			result += fixed_output[0] * 1000 + fixed_output[1] * 100 + fixed_output[2] * 10 + fixed_output[3]
		else:
			result += sum(1 for o in fixed_output if o in (1, 4, 7, 8))
		# print(patterns)
		# print(output)
		# print(mapping)
		# print(fixed_output)
		# if True:
		# 	break

	print(result)

if __name__ == '__main__':
	main()
