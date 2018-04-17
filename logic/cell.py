import operator


class Cell:
    def __init__(self, *coords):
        if not isinstance(coords[0], int):
            coords = coords[0]
        self.coords = tuple(coords)
        self.dim = len(coords)

    @staticmethod
    def basis_cell(direction, dim):
        res = [0] * dim
        res[direction] = 1
        return Cell(res)

    def __add__(self, other):
        return Cell(tuple(map(operator.__add__, self.coords, other.coords)))

    def __mul__(self, other):
        if isinstance(other, int):
            return Cell([x * other for x in self.coords])

    def __sub__(self, other):
        return self + other * (-1)

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)

    def __getitem__(self, key):
        return self.coords[key]

    def __str__(self):
        return '({})'.format(', '.join(map(str, self.coords)))
