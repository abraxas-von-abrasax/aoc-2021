from enum import Enum

from src.util.file_utils import parse_file


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Coordinates(self.x, self.y)


class LineDirection(Enum):
    HORIZONTAL_RIGHT = 1
    HORIZONTAL_LEFT = 2

    VERTICAL_UP = 3
    VERTICAL_DOWN = 4

    DIAGONAL_UP_RIGHT = 5
    DIAGONAL_UP_LEFT = 6
    DIAGONAL_DOWN_RIGHT = 7
    DIAGONAL_DOWN_LEFT = 8


class Line:
    def __init__(self, start: Coordinates, end: Coordinates):
        self.start = start.copy()
        self.end = end.copy()
        if start.x == end.x and start.y != end.y:
            if start.y < end.y:
                self.direction = LineDirection.VERTICAL_DOWN
            else:
                self.direction = LineDirection.VERTICAL_UP
        elif start.x != end.x and start.y == end.y:
            if start.x < end.x:
                self.direction = LineDirection.HORIZONTAL_RIGHT
            else:
                self.direction = LineDirection.HORIZONTAL_LEFT
        else:
            if start.x < end.x:
                # from left to right
                if start.y < end.y:
                    # from top to bottom
                    self.direction = LineDirection.DIAGONAL_DOWN_RIGHT
                else:
                    self.direction = LineDirection.DIAGONAL_UP_RIGHT
            else:
                if start.y < end.y:
                    self.direction = LineDirection.DIAGONAL_DOWN_LEFT
                else:
                    self.direction = LineDirection.DIAGONAL_UP_LEFT

    def is_diagonal(self):
        return self.direction == LineDirection.DIAGONAL_UP_RIGHT \
               or self.direction == LineDirection.DIAGONAL_UP_LEFT \
               or self.direction == LineDirection.DIAGONAL_DOWN_RIGHT \
               or self.direction == LineDirection.DIAGONAL_DOWN_LEFT

    def print(self):
        print(f"[{self.start.x},{self.start.y}] -> [{self.end.x},{self.end.y}]")

    @staticmethod
    def traverse_line(coordinates: Coordinates, direction: LineDirection):
        if direction == LineDirection.HORIZONTAL_RIGHT:
            coordinates.x += 1
        elif direction == LineDirection.HORIZONTAL_LEFT:
            coordinates.x -= 1
        elif direction == LineDirection.VERTICAL_UP:
            coordinates.y -= 1
        elif direction == LineDirection.VERTICAL_DOWN:
            coordinates.y += 1
        elif direction == LineDirection.DIAGONAL_UP_RIGHT:
            coordinates.x += 1
            coordinates.y -= 1
        elif direction == LineDirection.DIAGONAL_UP_LEFT:
            coordinates.x -= 1
            coordinates.y -= 1
        elif direction == LineDirection.DIAGONAL_DOWN_RIGHT:
            coordinates.x += 1
            coordinates.y += 1
        elif direction == LineDirection.DIAGONAL_DOWN_LEFT:
            coordinates.x -= 1
            coordinates.y += 1
        else:
            raise Exception('Unknown direction')


class CoordinatesMap:
    def __init__(self):
        self.__map = {}

    def has_coordinates(self, coordinates: Coordinates) -> bool:
        return coordinates.x in self.__map and \
               coordinates.y in self.__map[coordinates.x]

    def set_line(self, line: Line) -> None:
        current = line.start.copy()
        while current != line.end:
            self.__set_coordinates(current)
            Line.traverse_line(current, line.direction)
        self.__set_coordinates(line.end)

    def get_duplicates_count(self) -> int:
        count = 0
        for x in self.__map.values():
            for point in x.values():
                if point > 1:
                    count += 1
        return count

    def print(self):
        for x, v in self.__map.items():
            print(f"{x}: ", end = '')
            print(v)

    def __set_coordinates(self, coords: Coordinates):
        if self.has_coordinates(coords):
            self.__map[coords.x][coords.y] += 1
        else:
            if coords.x in self.__map:
                self.__map[coords.x][coords.y] = 1
            else:
                self.__map[coords.x] = {coords.y: 1}


class LineStore:
    def __init__(self):
        self.lines = []
        self.next = 0

    def has_next(self):
        return self.next < len(self.lines)

    def get_next(self):
        line = self.lines[self.next]
        self.next += 1
        return line

    def add(self, line: Line):
        self.lines.append(line)

    def reset(self):
        self.next = 0

    def print(self):
        for line in self.lines:
            line.print()


def init(inputs) -> LineStore:
    store = LineStore()
    for line in inputs:
        start, end = line.split(' -> ')
        start_x, start_y = start.split(',')
        start_x, start_y = [int(start_x), int(start_y)]
        end_x, end_y = end.split(',')
        end_x, end_y = [int(end_x), int(end_y)]
        start, end = [Coordinates(start_x, start_y), Coordinates(end_x, end_y)]
        store.add(Line(start, end))
    return store


def solve(store, consider_diagonals = False):
    coords_map = CoordinatesMap()
    while store.has_next():
        line = store.get_next()
        if not consider_diagonals and line.is_diagonal():
            continue
        coords_map.set_line(line)
    return coords_map.get_duplicates_count()


if __name__ == '__main__':
    lines = parse_file('./src/d5/input.txt')
    line_store = init(lines)
    res_part_1 = solve(line_store)
    print('Part 1:', res_part_1)
    line_store.reset()
    res_part_2 = solve(line_store, True)
    print('Part 2:', res_part_2)
