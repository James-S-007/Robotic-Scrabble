'''
    File taken from: https://github.com/adampirog/Scrabble and slightly modified
    All credit goes to the original author
'''

import fileinput
import pickle
from time import time


def timer(func):
    def f(*args, **kwargs):
        before = time()
        result = func(*args, **kwargs)
        after = time()
        print('Time elapsed: '+str(after-before)+" s")
        return result
    return f


class TrieNode:

    def __init__(self):
        self.children = [None]*26

        self.isTerminal = False


class Trie:

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def char_to_index(self, char):
        return ord(char)-ord('a')

    def insert(self, key):
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self.char_to_index(key[level])

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.get_node()
            pCrawl = pCrawl.children[index]

        pCrawl.isTerminal = True

    def is_word(self, key):
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self.char_to_index(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl != None and pCrawl.isTerminal


# imports a dictionary from txt format and creates Trie file
@timer
def import_dictionary(input, output):
    tree = Trie()

    for line in fileinput.input(input):
        tree.insert(str.strip(line))

    fileinput.close()
    if(output == ""):
        return tree

    filehandler = open(output, 'wb')
    pickle.dump(tree, filehandler)
    filehandler.close()
    return tree


# loads a dictionary from a binary file
@timer
def load_dictionary(file):
    filehandler = open(file, 'rb')
    dictionary = pickle.load(filehandler)
    filehandler.close()
    return dictionary


def index_to_char(index):
    return chr(index+ord('a'))


def char_to_index(char):
    return ord(char)-ord('a')

# decorator timer
