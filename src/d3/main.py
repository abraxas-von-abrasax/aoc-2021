from enum import Enum

from src.util.file_utils import parse_file


class LifeSupportType(Enum):
    OXYGEN_GENERATOR = 1
    CO2_SCRUBBER = 2


def part_1(inputs):
    def run_iteration():
        ones = 0
        zeros = 0

        for i, num in enumerate(inputs):
            if num[0] == '1':
                ones += 1
            else:
                zeros += 1

            inputs[i] = num[1:]

        return '1' if ones < zeros else '0'

    gamma = ''

    while inputs[0]:
        gamma += run_iteration()

    epsilon = ''

    for char in gamma:
        if char == '1':
            epsilon += '0'
        else:
            epsilon += '1'

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    return gamma * epsilon


def part_2(inputs):
    def find_val(numbers: list[str], type: LifeSupportType) -> str:
        tmp = numbers.copy()
        cur_pos = 0

        def run_iteration():
            indices_ones = []
            indices_zeros = []

            for i, num in enumerate(tmp):
                if num[cur_pos] == '1':
                    indices_ones.append(i)
                else:
                    indices_zeros.append(i)

            if type == LifeSupportType.OXYGEN_GENERATOR:
                return indices_ones if len(indices_ones) >= len(indices_zeros) else indices_zeros
            else:
                return indices_ones if len(indices_ones) < len(indices_zeros) else indices_zeros

        while len(tmp) > 1:
            filter_indices = run_iteration()
            tmp = [tmp[i] for i in filter_indices]
            cur_pos += 1

        return tmp[0]

    oxygen_generator, co2_scrubber = (find_val(inputs, LifeSupportType.OXYGEN_GENERATOR),
                                      find_val(inputs, LifeSupportType.CO2_SCRUBBER))

    oxygen_generator = int(oxygen_generator, 2)
    co2_scrubber = int(co2_scrubber, 2)

    return oxygen_generator * co2_scrubber


if __name__ == '__main__':
    lines = parse_file('./src/d3/input.txt')
    result = (part_1(lines.copy()), part_2(lines.copy()))
    print('Part 1:', result[0])
    print('Part 2:', result[1])
