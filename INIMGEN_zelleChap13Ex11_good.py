# GOOD #
import itertools
class WordTruer:
    def __init__(self, dictionary, string):
        # Initialization of the WordTruer class object
        self.dictionary = dictionary  # Path to the dictionary file
        self.string = string  # String to find in dictionary
        # Generate anagrams from the input string
        self.anagrams = {}
        self.found_words = []  # List to store words found in the dictionary
        self.dictionary_words = []  # List to store words from the dictionary file

    def read_dictionary(self):
        try:
            # Read words from the dictionary file
            with open(self.dictionary, 'r') as f:
                for word in f.readlines():
                    self.dictionary_words.append(word.strip())
        except FileNotFoundError:
            print("File not found.")

    def generate_anagrams(self, s):
        # Generate all possible permutations of the input string to create anagrams
        return {''.join(anagram): None for i in range(len(s)) for anagram in itertools.permutations(s)}

    # TODO: Incorporate gaddag algorithm to speed up check anagrams
    def gaddag(self):
        pass

    def check_anagrams(self):
        # Check each generated anagram if it exists in the dictionary
        self.anagrams = self.generate_anagrams(self.string)
        self.found_words = [an for an in self.anagrams if an in self.dictionary_words]


    def summary(self):
        for word in self.found_words:
            print(word)

    def find_anagrams(self):
        self.read_dictionary()
        self.check_anagrams()
        self.summary()

WordTruer('eng_dictionary.txt', 'fish').find_anagrams()