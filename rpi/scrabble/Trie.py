'''
    File taken from: https://github.com/adampirog/Scrabble and slightly modified
    All credit goes to the original author
'''

from time import time

# timer decorator
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


def index_to_char(index):
    return chr(index+ord('a'))


def char_to_index(char):
    return ord(char)-ord('a')
