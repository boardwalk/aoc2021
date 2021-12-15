import sys

def main():
    lines = sys.stdin.readlines()

    template = lines[0].strip()

    rules = []
    for line in lines[2:]:
        left, right = line.strip().split(' -> ')
        assert len(left) == 2
        assert len(right) == 1
        rules.append((left, right))

    print(f'Template:     {template}')

    print('Doing insertions...')
    sequence = template
    for i in range(40):
        print(f'On step {i}, sequence len = {len(sequence)}')
        insertions = []
        for (left, right) in rules:
            idx = 0
            while True:
                idx = sequence.find(left, idx)
                if idx < 0:
                    break
                insertions.append((idx + 1, right))
                idx = idx + 1

        insertions.sort()

        for j, (insert_idx, value) in enumerate(insertions):
            sequence = sequence[:insert_idx + j] + value + sequence[insert_idx + j:]

        # print(f'After step {i + 1}: {sequence}')

    print('Counting...')
    counts = {}
    for c in sequence:
        try:
            counts[c] += 1
        except KeyError:
            counts[c] = 1

    print('Sorting counts...')
    sorted_counts = [(count, elem) for elem, count in counts.items()]
    sorted_counts.sort()

    print(sorted_counts[-1][0] - sorted_counts[0][0])

if __name__ == '__main__':
    main()
