from typing import Optional

from src.util.file_utils import parse_file


class Field:
    def __init__(self, rows: list[str]):
        self.marked_as_won = False
        self.rows: list[list[list[int, bool]]] = []
        for row in rows:
            row_nums = [[int(num), False] for num in list(filter(None, row.split(' ')))]
            self.rows.append(row_nums)

    def print_rows(self):
        print(self.rows)

    def mark_num(self, num: int):
        for x in self.rows:
            for y in x:
                if y[0] == num:
                    y[1] = True

    def has_won(self) -> (bool, Optional[int]):
        # Check rows
        for row in self.rows:
            is_winning_row = True
            for item in row:
                if not item[1]:
                    is_winning_row = False
                    break
            if is_winning_row:
                return True
        # Check columns
        for index in range(0, 5):
            is_winning_col = True
            for row in self.rows:
                if not row[index][1]:
                    is_winning_col = False
                    break
            if is_winning_col:
                return True
        return False

    def get_unmarked_score(self) -> int:
        unmarked_score = 0
        for row in self.rows:
            for el in row:
                if not el[1]:
                    unmarked_score += el[0]
        return unmarked_score

    def clear(self):
        for row in self.rows:
            for el in row:
                el[1] = False


class Game:
    def __init__(self, draws: list[int], fields: list[Field]):
        self.draws = draws
        self.fields = fields

    def reset(self):
        for field in self.fields:
            field.clear()

    def has_unfinished_fields(self):
        for field in self.fields:
            if not field.marked_as_won:
                return True
        return False


def init(inputs: list[str]) -> Game:
    drawn_nums = [int(num) for num in inputs.pop(0).split(',')]
    inputs.pop(0)

    bingo_fields: list[Field] = []

    cur_bingo_field_rows: list[str] = []

    def create_bingo_field():
        nonlocal cur_bingo_field_rows
        new_field = Field(cur_bingo_field_rows)
        bingo_fields.append(new_field)
        cur_bingo_field_rows = []

    for row in inputs:
        if not row:
            create_bingo_field()
            continue
        cur_bingo_field_rows.append(row)

    create_bingo_field()

    return Game(drawn_nums, bingo_fields)


def part_1() -> int:
    for drawn_num in game.draws:
        for field in game.fields:
            field.mark_num(drawn_num)
            if field.has_won():
                return field.get_unmarked_score() * drawn_num


def part_2() -> int:
    for drawn_num in game.draws:
        for field in game.fields:
            if field.marked_as_won:
                continue
            field.mark_num(drawn_num)
            if field.has_won():
                field.marked_as_won = True
            if not game.has_unfinished_fields():
                return field.get_unmarked_score() * drawn_num


if __name__ == '__main__':
    lines = parse_file('./src/d4/input.txt')
    game = init(lines)
    res_part_1 = part_1()
    print('Part 1:', res_part_1)
    game.reset()
    res_part_2 = part_2()
    print('Part 2:', res_part_2)
