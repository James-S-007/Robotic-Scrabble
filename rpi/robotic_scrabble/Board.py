'''

'''
import csv

class Board:
    def __init__(self, n=15):
        self.board = ['-' for _ in range(15)]

    # Outputs current board to terminal
    def draw(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], " ", end='')
            print()
        print()

    # Loads board from csv file
    # Empty tiles in file are denoted by '-'
    def import_board(self, file):
        self.board = list(csv.reader(open(file)))
