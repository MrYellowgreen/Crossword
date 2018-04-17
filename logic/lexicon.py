class Lexicon:
    def __init__(self, words, progressbar=None):
        self.all_words = set()
        self.lengths = {}
        counter = 0
        for word in words:
            self.add_word(word)
            counter += 1
            if counter % 5000 == 0 and progressbar:
                progressbar('{}/{} words added'.format(counter, len(words)))

    def add_word(self, word):
        if not word or word in self.all_words:
            return
        self.all_words.add(word)
        if len(word) not in self.lengths:
            self.lengths[len(word)] = {}
        for mask in self.get_all_simple_masks(word):
            if mask not in self.lengths[len(word)]:
                self.lengths[len(word)][mask] = []
            self.lengths[len(word)][mask].append(word)

    def get_all_simple_masks(self, word):
        yield (None,) * len(word)
        for i in range(len(word)):
            mask = [None] * len(word)
            mask[i] = word[i]
            yield tuple(mask)

    def __call__(self, mask):
        mask = tuple(mask)
        if len(mask) not in self.lengths:
            return []
        simple_mask = self.get_simple_version(mask)
        if simple_mask not in self.lengths[len(mask)]:
            return []
        for word in self.lengths[len(mask)][simple_mask]:
            if self.mask_is_suitable_for_word(mask, word):
                yield word

    def get_simple_version(self, mask):
        res = [None] * len(mask)
        for i in range(len(mask)):
            if mask[i] is not None:
                res[i] = mask[i]
                break
        return tuple(res)

    def mask_is_suitable_for_word(self, mask, word):
        for pair in zip(mask, word):
            if pair[0] is not None and pair[0] != pair[1]:
                return False
        return True
