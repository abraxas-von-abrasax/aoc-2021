from typing import Optional

from src.util.file_utils import parse_file


def part_1(inputs):
    last: Optional[int] = None
    result = 0

    for line in inputs:
        line = int(line)
        if last and line > last:
            result += 1
        last = line

    return result


def part_2(inputs):
    window_scores = []

    for i, line in enumerate(inputs):
        if (i + 1) < len(inputs) and (i + 2) < len(inputs):
            window_scores.append(int(line) + int(inputs[i + 1]) + int(inputs[i + 2]))

    return part_1(window_scores)


if __name__ == '__main__':
    lines = parse_file('./src/d1/input.txt')
    result_part_1 = part_1(lines)
    result_part_2 = part_2(lines)
    print('Part 1:', result_part_1)
    print('Part 2:', result_part_2)
