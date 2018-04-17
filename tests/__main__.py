import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import logic
from logic.lexicon import Lexicon
from logic.cell import Cell
from logic.word import Word, RealWord, WordsFromGridGetter
from logic.geometry import Geometry
from logic.solver import Solver


class TestLexicon(unittest.TestCase):
    def test_lexicon(self):
        lexicon = Lexicon(['abc', 'an', 'ant', 'one'])
        self.assertEqual(list(lexicon(['a', None, None])), ['abc', 'ant'])
        self.assertEqual(list(lexicon([None, None, None])),
                         ['abc', 'ant', 'one'])
        self.assertEqual(list(lexicon(['a', None, None, None])), [])
        self.assertEqual(list(lexicon([None, 'n', 't'])), ['ant'])


class TestCell(unittest.TestCase):
    def test_cell(self):
        cells = [Cell((2, 5, 3)), Cell(1, 2, -1)]
        self.assertEqual(cells[0].dim, 3)
        self.assertEqual(cells[0] + Cell.basis_cell(1, 3), Cell((2, 6, 3)))
        self.assertEqual(cells[0] - cells[1], Cell((1, 3, 4)))
        self.assertEqual(cells[0] * 2, Cell((4, 10, 6)))
        self.assertEqual(str(cells[0]), '(2, 5, 3)')


class TestWords(unittest.TestCase):
    def test_word(self):
        word = Word((1, 2), 1, 3)
        self.assertEqual(str(word), '(1, 2), 1, 3')
        cells = [Cell(1, 2), Cell(1, 3), Cell(1, 4)]
        counter = 0
        for cell in word:
            self.assertEqual(cell, cells[counter])
            counter += 1

    def test_real_word(self):
        real_word = RealWord(Word((2, 95, 0), 0, 6))
        self.assertEqual(real_word.has_value(), False)
        real_word.set_values(['abcdef', 'qwerty', 'qazxsw'])
        self.assertTrue(real_word.has_value())
        self.assertEqual(real_word.value, 'abcdef')
        real_word.next_value()
        self.assertEqual(real_word.letter_by_cell(Cell(4, 95, 0)), 'e')
        real_word.delete_values()
        self.assertEqual(real_word.has_value(), False)

    def test_words_from_grid_getter(self):
        getter = WordsFromGridGetter(['...', '.#.', '...'])
        words = getter.get_words()
        self.assertEqual(set(words), set((Word((0, 0), 1, 3),
                         Word((0, 0), 0, 3), Word((0, 2), 0, 3),
                         Word((2, 0), 1, 3))))


class TestGeometry(unittest.TestCase):
    def test_geometry(self):
        words = [Word((1, 1, 1), 0, 4), Word((2, 1, 0), 2, 2),
                 Word((2, 0, 1), 1, 100), Word((2, 70, 1), 0, 5)]
        geom = Geometry(words)
        self.assertEqual(geom.cells[Cell(4, 1, 1)], {0: Word((1, 1, 1), 0, 4)})
        self.assertEqual(geom.cells[Cell(2, 70, 1)],
                         {0: Word((2, 70, 1), 0, 5),
                         1: Word((2, 0, 1), 1, 100)})
        self.assertEqual(geom.cells[Cell(2, 1, 1)], {0: Word((1, 1, 1), 0, 4),
                         1: Word((2, 0, 1), 1, 100), 2: Word((2, 1, 0), 2, 2)})
        self.assertEqual(geom.size, Cell(7, 100, 2))


class TestSolver(unittest.TestCase):
    def test_all_outputs(self):
        lexicon = Lexicon(['aaa', 'abc', 'ccc', 'dd', 'ehh', 'gfy'])
        words = [Word((0, 0), 1, 3), Word((0, 1), 0, 3), Word((2, 0), 1, 3)]
        solver = Solver(Geometry(words), lexicon)
        answers = solver.solve(2)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].words, {Word((0, 0), 1, 3): 'aaa',
                         Word((0, 1), 0, 3): 'abc', Word((2, 0), 1, 3): 'ccc'})
        self.assertEqual(answers[0].string(), '(0, 0), 1, 3: aaa\n' +
                         '(0, 1), 0, 3: abc\n(2, 0), 1, 3: ccc\n')
        self.assertEqual(answers[0].string(in_grid=True), 'a#c\nabc\na#c\n')

    def test_input_from_grid_and_2_answers(self):
        lexicon = Lexicon(['ab', 'bc', 'ad', 'dc', 'z', 'zz', 'zzz'])
        words = logic.word.WordsFromGridGetter(['..', '..']).get_words()
        solver = Solver(Geometry(words), lexicon)
        answers = solver.solve(2)
        self.assertEqual(len(answers), 2)
        expected_answer_1 = {Word((0, 0), 0, 2): 'ab',
                             Word((0, 0), 1, 2): 'ad',
                             Word((0, 1), 0, 2): 'dc',
                             Word((1, 0), 1, 2): 'bc'}
        expected_answer_2 = {Word((0, 0), 0, 2): 'ad',
                             Word((0, 0), 1, 2): 'ab',
                             Word((0, 1), 0, 2): 'bc',
                             Word((1, 0), 1, 2): 'dc'}
        try:
            self.assertEqual(answers[0].words, expected_answer_1)
            self.assertEqual(answers[1].words, expected_answer_2)
        except Exception:
            self.assertEqual(answers[0].words, expected_answer_2)
            self.assertEqual(answers[1].words, expected_answer_1)

    def test_third_dimension(self):
        lexicon = Lexicon(['a b', 'c d', 'e f', 'la', 'lol', 'ff'])
        words = [Word((0, 1, 1), 0, 3), Word((1, 0, 1), 1, 3),
                 Word((1, 1, 0), 2, 3), Word((0, 0, 1), 0, 2),
                 Word((1, 0, 2), 1, 2)]
        solver = Solver(Geometry(words), lexicon)
        answers = solver.solve(1)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].words, {Word((0, 1, 1), 0, 3): 'c d',
                         Word((1, 0, 1), 1, 3): 'a b',
                         Word((1, 1, 0), 2, 3): 'e f',
                         Word((0, 0, 1), 0, 2): 'la',
                         Word((1, 0, 2), 1, 2): 'ff'})

    def test_no_solution(self):
        lexicon = Lexicon(['i', "don't", 'think', 'so'])
        words = logic.word.WordsFromGridGetter(['...#....']).get_words()
        solver = Solver(Geometry(words), lexicon)
        answers = solver.solve(1)
        self.assertEqual(len(answers), 0)


if __name__ == '__main__':
    unittest.main()
