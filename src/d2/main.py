from src.util.file_utils import parse_file


def part_1(inputs):
    horizontal_pos = 0
    depth = 0

    for (cmd, value) in inputs:
        if cmd == 'forward':
            horizontal_pos += value
        elif cmd == 'down':
            depth += value
        elif cmd == 'up':
            depth -= value

    return horizontal_pos * depth


def part_2(inputs):
    horizontal_pos = 0
    depth = 0
    aim = 0

    for (cmd, value) in inputs:
        if cmd == 'forward':
            horizontal_pos += value
            depth += (aim * value)
        elif cmd == 'down':
            aim += value
        elif cmd == 'up':
            aim -= value

    return horizontal_pos * depth


def prepare_input(inputs) -> list[tuple[str, int]]:
    return [(cmd, int(val)) for cmd, val in [line.split() for line in inputs]]


if __name__ == '__main__':
    lines = prepare_input(parse_file('./src/d2/input.txt'))
    results = (part_1(lines), part_2(lines))
    print('Part 1:', results[0])
    print('Part 2:', results[1])
