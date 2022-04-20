import pickle

from scrabble.Trie import Trie

class GameRules:
    def __init__(self, dictionary):
        self.dictionary = self.import_dictionary(dictionary)
        self.letter_values = {
            "a": 1,
            "b": 3,
            "c": 3,
            "d": 2,
            "e": 1,
            "f": 4,
            "g": 2,
            "h": 4,
            "i": 1,
            "j": 8,
            "k": 5,
            "l": 1,
            "m": 3,
            "n": 1,
            "o": 1,
            "p": 3,
            "q": 10,
            "r": 1,
            "s": 1,
            "t": 1,
            "u": 1,
            "v": 4,
            "w": 4,
            "x": 8,
            "y": 4,
            "z": 10,
        }

    def validate_word(self, word):
        return self.dictionary.is_word(word)


    # imports a dictionary from txt format and creates Trie
    # Optionally saves serialized Trie to file for quick loading at next boot
    def import_dictionary(self, dict_file, dict_outfile=None):
        tree = Trie()
        with open(dict_file) as f:
            for line in f:
                tree.insert(str.strip(line))

        if dict_outfile:
            with open(dict_outfile, 'wb') as f:
                pickle.dump(tree, f)
                
        return tree

    # loads previously serialized dictionary saved in file
    def load_dictionary(self, file):
        with open(file, 'rb') as f:
            dictionary = pickle.load(f)
        
        return dictionary


    def score_word(self, word):
        sum = 0
        for letter in word:
            sum += self.letter_values[letter]
        return sum
