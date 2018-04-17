from logic.cell import Cell


class Geometry:
    def __init__(self, words):
        self.cells = {}
        if words:
            self.dim = words[0].dim
        else:
            self.dim = 0
        self.size = Cell([1] * self.dim)
        self.words = words
        for word in words:
            self.add_word(word)

    def add_word(self, word):
        for cell in word:
            if cell not in self.cells:
                self.cells[cell] = {}
                self._update_size(cell)
            self.cells[cell][word.direction] = word

    def _update_size(self, cell):
        for i in range(self.dim):
            self.size += (Cell.basis_cell(i, self.dim) *
                          max(0, 1 + cell.coords[i] - self.size.coords[i]))
