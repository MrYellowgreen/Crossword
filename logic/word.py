from logic.cell import Cell


class Word:
    def __init__(self, begin_coords, direction, length):
        self.begin_cell = Cell(begin_coords)
        self.direction = direction
        self._len = length
        self.dim = len(begin_coords)

    def __len__(self):
        return self._len

    def __iter__(self):
        res = []
        cell = self.begin_cell
        step = Cell.basis_cell(self.direction, self.dim)
        for i in range(len(self)):
            res.append(cell)
            cell += step
        return iter(res)

    def __eq__(self, other):
        return ((self.begin_cell, self.direction, len(self)) ==
                (other.begin_cell, other.direction, len(other)))

    def __hash__(self):
        return hash(self.begin_cell)

    def ordering_key(self):
        res = 0
        for coord in self.begin_cell.coords:
            res += coord
        return res

    def ordering_key_for_answer(self):
        return list(self.begin_cell.coords) + [self.direction, len(self)]

    def __str__(self):
        return '{}, {}, {}'.format(self.begin_cell, self.direction, len(self))


class RealWord:
    def __init__(self, word):
        self.word = word
        self.values = iter([])
        self.value = None

    def has_value(self):
        return self.value is not None

    def set_values(self, values):
            self.values = iter(values)
            try:
                self.value = next(self.values)
            except StopIteration:
                self.values = []
                self.value = None

    def delete_values(self):
        self.values = []
        self.value = None

    def letter_by_cell(self, cell):
        cells_diff = cell - self.word.begin_cell
        letter_num = 0
        for coord in cells_diff.coords:
            if coord > 0:
                letter_num = coord
        return self.value[letter_num]

    def next_value(self):
        try:
            self.value = next(self.values)
        except StopIteration:
            self.value = None
            self.values = []


class WordsFromGridGetter:
    def __init__(self, grid, opened='.', closed='#'):
        self.grid = grid
        self.opened = opened
        self.closed = closed

    def get_words(self):
        res = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == self.opened:
                    res += list(self._get_words_from_cell(x, y))
        return res

    def _get_words_from_cell(self, x, y):
        if (len(self.grid[y]) > x + 1 and self.grid[y][x + 1] ==
                self.opened and (x == 0 or self.grid[y][x - 1] ==
                                 self.closed)):
            yield self._get_horizontal_word(x, y)
        if (len(self.grid) > y + 1 and self.grid[y + 1][x] == self.opened and
               (y == 0 or self.grid[y - 1][x] == self.closed)):
            yield self._get_vertical_word(x, y)

    def _get_vertical_word(self, x, y):
        y_end = y + 1
        while len(self.grid) > y_end and self.grid[y_end][x] == self.opened:
            y_end += 1
        return Word((x, y), 1, y_end - y)

    def _get_horizontal_word(self, x, y):
        x_end = x + 1
        while len(self.grid[y]) > x_end and self.grid[y][x_end] == self.opened:
            x_end += 1
        return Word((x, y), 0, x_end - x)
