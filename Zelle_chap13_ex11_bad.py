# BAD CODE #
class WordTruer:
    def __init__(self, dictionary, string):
        self.dictionary = dictionary
        self.string = string
        self.anagrams = self.permute(self.string)
        self.twords = []
        self.dwords = []
        self.read_dict()

        self.check_anagrams()
        self.summary()

    def read_dict(self):
        self.dwords = [line.strip() for line in open(self.dictionary, 'r')]

    def permute(self, s):
        p = []
        if len(s) <= 1:
            p = [s]

        else:
            for i, let in enumerate(s):
                for perm in self.permute(s[:i] + s[i + 1:]):
                    p += [let + perm]
        return p

    def gaddag(self):
        pass

    def check_anagrams(self):
        for an in self.anagrams:
            if self.search(an):
                self.twords.append(an)

    def search(self, inword):
        for word in self.dwords:
            if inword == word:
                return True
        return False

    def summary(self):
        for word in self.twords:
            print(word)


WordTruer('eng_dictionary.txt', 'fish')