import sys

PART2 = True

def main():
    lines = sys.stdin.readlines()

    template = lines[0].strip()

    rules = {} # XY -> XAY
    for line in lines[2:]:
        left, right = line.strip().split(' -> ')
        assert len(left) == 2
        assert len(right) == 1
        rules[left] = left[0] + right + left[1]

    rules_2 = {} # XY -> [XY, ...]
    for key, expanded in rules.items():
        subs = []
        if expanded[:2] in rules:
            subs.append(expanded[:2])
        if expanded[1:] in rules:
            subs.append(expanded[1:])
        rules_2[key] = subs

    template_2 = {key: 0 for key in rules} # XY -> count
    for key in rules:
        idx = 0
        while True:
            idx = template.find(key, idx)
            if idx < 0:
                break
            template_2[key] += 1
            idx = idx + 1

    if PART2:
        num_steps = 10
    else:
        num_steps = 40

    for i in range(num_steps):
        more = {key: 0 for key in rules}

        for key, count in template_2.items():
            for sub in rules_2[key]:
                more[sub] += count

        template_2 = more

    counts = {}
    for key, count in template_2.items():
        for elem in key:
            try:
                counts[elem] += count
            except KeyError:
                counts[elem] = count

    for key in counts:
        counts[key] = int(counts[key] / 2 + 0.5)

    sorted_counts = [(count, elem) for elem, count in counts.items()]
    sorted_counts.sort()

    print(sorted_counts[-1][0] - sorted_counts[0][0])

if __name__ == '__main__':
    main()
