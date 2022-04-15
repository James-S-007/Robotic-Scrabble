from random import randint
from pprint import pprint

class Storage:
    def __init__(self, rows=15, cols=2):
        self.rows = rows
        self.cols = cols
        self.letters = [[1 for _ in range(cols)] for _ in range(rows)]
        self.remaining_letters = self.rows * self.cols

    def unroll(self, idx):
        row = idx // self.cols
        col = idx - row*self.cols
        return row, col

    # returns -1, -1 if no remaining letters
    def generate_letter(self):
        if self.remaining_letters < 1:
            return -1, -1
        x,y = self.unroll(randint(0, self.rows*self.cols - 1))
        while not self.letters[x][y]:
            x,y = self.unroll(randint(0, self.rows*self.cols - 1))
        self.letters[x][y] = None
        self.remaining_letters -= 1
        return x,y

    def generate_letters(self, num_letters):
        letter_indices = []
        for i in range(0, num_letters):
            letter_indices.append(self.generate_letter())
        return letter_indices
