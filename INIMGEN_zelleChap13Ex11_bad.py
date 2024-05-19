# BAD #
class WordTruer:
    def __init__(self, dictionary, string):
        self.dictionary = dictionary
        self.string = string
        self.anagrams = self.permute(self.string)
        self.twords = []
        self.dwords = []

        self.check_anagrams()
        self.summary()

    def permute(self, s):
        if len(s) == 1 or len(s) == 0:
            return [s]
        else:
            p = []
            for w in self.permute(s[1:]):
                for pos in range(len(w) + 1):
                    p.append(w[:pos]+s[0]+w[pos:])
        return p


    def gaddag(self):
        return 'todo'

    def check_anagrams(self):
        with open(self.dictionary, 'r') as f:
            for word in f.readlines():
                self.dwords.append(word.strip())
        for an in self.anagrams:
            for word in self.dwords:
                if an == word:
                    if an not in self.twords:
                        self.twords.append(an)


    def linear_search(self, arr, inword):
        for word in arr:
            if word == inword:
                return True
        return False


    def summary(self):
        total_words = len(self.dwords)
        total_anagrams = len(self.anagrams)
        total_true_words = len(self.twords)
        print(f"Total words in dictionary: {total_words}")
        print(f"Total anagrams generated: {total_anagrams}")
        print(f"Total true words found: {total_true_words}")
        for word in self.twords:
            print(word)


WordTruer('eng_dictionary.txt', 'fish')