#!/usr/bin/env python3
import binascii
import sys
from functools import reduce

PART2 = True
version_sum = 0

class BitReader:
    def __init__(self, hex_data: str) -> None:
        self._data = binascii.a2b_hex(hex_data)
        self._position = 0

    def read(self, num_bits: int) -> int:
        result = 0

        while num_bits > 0:
            cur_byte = self._position // 8
            cur_bit = self._position % 8

            if cur_bit + num_bits > 8:
                bits_to_read = 8 - cur_bit
            else:
                bits_to_read = num_bits

            mask =  (1 << bits_to_read) - 1
            bits = (self._data[cur_byte] >> (8 - cur_bit - bits_to_read)) & mask

            result = (result << bits_to_read) | bits

            self._position += bits_to_read
            num_bits -= bits_to_read

        return result

    @property
    def position(self) -> int:
        return self._position

def read_packet(reader: BitReader, *, indent: str = '') -> int:
    version = reader.read(3)
    type = reader.read(3)
    print(f'{indent}version={version} type={type}')

    global version_sum
    version_sum += version

    if type == 0x4: # literal
        value = 0
        while True:
            bits = reader.read(5)
            value = (value << 4) | (bits & 0b1111)
            if bits & 0b10000 == 0:
                break
        print(f'{indent}literal, value={value}')
        return value
    else: # operator packet
        if type == 0: # sum
            oper = lambda lst: sum(lst)
        elif type == 1: # product
            oper = lambda lst: reduce(lambda a, b: a * b, lst, 1)
        elif type == 2: # min
            oper = lambda lst: min(lst)
        elif type == 3: # max
            oper = lambda lst: max(lst)
        elif type == 5: # greater than
            oper = lambda lst: 1 if lst[0] > lst[1] else 0
        elif type == 6: # less than
            oper = lambda lst: 1 if lst[0] < lst[1] else 0
        elif type == 7: # equal
            oper = lambda lst: 1 if lst[0] == lst[1] else 0
        else:
            raise RuntimeError('invalid operator packet type')

        values = []
        length_type_id = reader.read(1)
        if length_type_id == 0:
            length_in_bits = reader.read(15)
            print(f'{indent}operator, length_in_bits={length_in_bits}')
            start = reader.position
            while reader.position < start + length_in_bits:
                values.append(read_packet(reader, indent=indent + ' '))
        else:
            length_in_packets = reader.read(11)
            print(f'{indent}operator, length_in_packets={length_in_packets}')
            for i in range(length_in_packets):
                values.append(read_packet(reader, indent=indent + ' '))

        return oper(values)

def main():
    reader = BitReader(sys.stdin.read())
    result = read_packet(reader)

    if PART2:
        print(result)
    else:
        print(version_sum)

if __name__ == '__main__':
    main()
