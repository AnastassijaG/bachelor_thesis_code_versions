# GOOD CODE #
class AnagramChecker:
    def __init__(self, dictionary_file, word):
        self.dictionary_file = dictionary_file
        self.word = word
        self.anagrams = self.generate_anagrams(self.word)
        self.true_words = []
        self.dictionary_words = []
        self.read_dictionary()

        self.check_anagrams()
        self.display_true_words()

    def read_dictionary(self):
        with open(self.dictionary_file, 'r') as f:
            self.dictionary_words = [line.strip() for line in f]

    def generate_anagrams(self, s):
        if len(s) <= 1:
            return [s]
        else:
            permutations = []
            for i, letter in enumerate(s):
                for permutation in self.generate_anagrams(s[:i] + s[i+1:]):
                    permutations.append(letter + permutation)
            return permutations

    def check_anagrams(self):
        for anagram in self.anagrams:
            if self.binary_search(self.dictionary_words, anagram):
                self.true_words.append(anagram)

    def binary_search(self, arr, word):
        if not arr:
            return False
        else:
            mid = len(arr) // 2
            dictionary_word = arr[mid]
            if word == dictionary_word:
                return True
            elif word < dictionary_word:
                return self.binary_search(arr[:mid], word)
            else:
                return self.binary_search(arr[mid+1:], word)

    def display_true_words(self):
        for word in self.true_words:
            print(word)


AnagramChecker('eng_dictionary.txt', 'fish')
