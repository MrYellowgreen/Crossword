from logic.word import Word, RealWord
from logic.cell import Cell


class Solver:
    def __init__(self, geometry, lexicon):
        self.geometry = geometry
        self.lexicon = lexicon
        self.used = dict([(x, False) for x in lexicon.all_words])
        self.words = geometry.words
        self.words.sort(key=Word.ordering_key)
        self.set_real_words()

    def set_real_words(self):
        res = {}
        for word in self.words:
            res[word] = RealWord(word)
        self.real_words = res

    def solve(self, answers_amount=1):
        word_num = 0
        answers = []
        while 0 <= word_num and len(answers) < answers_amount:
            if word_num == -1:
                break
            if word_num == len(self.words):
                answers.append(self.get_new_answer())
                word_num -= 1
                continue
            word = self.real_words[self.words[word_num]]
            if word.has_value():
                self.used[word.value] = False
                word.next_value()
            else:
                word.set_values(self.find_word_values(word))
            while (word.has_value() and self.used[word.value]):
                word.next_value()
            if not word.has_value():
                word.delete_values()
                word_num -= 1
                continue
            else:
                self.used[word.value] = True
                word_num += 1
                continue
        return answers

    def find_word_values(self, word):
        mask = []
        for cell in word.word:
            for direction in self.geometry.cells[cell]:
                if direction != word.word.direction:
                    other_word = self.real_words[
                        self.geometry.cells[cell][direction]]
                    if other_word.has_value():
                        mask.append(other_word.letter_by_cell(cell))
                        break
            else:
                mask.append(None)
        return self.lexicon(mask)

    def get_new_answer(self):
        return Answer(self)


class Answer:
    def __init__(self, solver):
        self.words = {}
        self.dim = solver.geometry.dim
        self.size = solver.geometry.size
        for real_word in solver.real_words.values():
            self.words[real_word.word] = real_word.value

    def string(self, in_grid=False):
        if not in_grid or self.dim != 2:
            res = ''
            ans_list = list(self.words)
            ans_list.sort(key=Word.ordering_key_for_answer)
            for word in ans_list:
                res += '{}: {}\n'.format(word, self.words[word])
            return res
        return self.string_in_grid()

    def string_in_grid(self):
        res = [['#'] * self.size[0] for _ in range(self.size[1])]
        for word in self.words:
            real_word = RealWord(word)
            real_word.set_values([self.words[word]])
            for cell in word:
                res[cell.coords[1]][cell.coords[0]] = (
                    real_word.letter_by_cell(cell))
        return '\n'.join(list(map(''.join, res))) + '\n'
