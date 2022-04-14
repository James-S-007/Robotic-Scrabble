import os.path

from Human import Human
from robotic_scrabble.Board import Board

def main():
    return


def test_word_validation():
    output = lambda actual, expected : print(f"{'PASS' if actual == expected else 'FAIL'}:\t\tActual:{actual}\tExpected{expected}")

    
    human = Human()
    board = Board()
    board.import_board(os.path.join(os.path.dirname(__file__), 'robotic_scrabble', 'board.csv'))
    # board.draw()
    move = {'c': [3, 6]}
    output(human.find_words_played(board, move), {(3, 6, 1): 'capple'})
    move = {'b': [4, 7], 'd': [4, 8]}
    output(human.find_words_played(board, move), {(4, 6, 0): 'abdm'})
    move = {'z': [4,5], 'y': [5,5]}
    output(human.find_words_played(board, move), {(4, 5, 0): 'za', (4, 5, 1): 'zy', (5, 5, 0): 'yp'})


if __name__ == '__main__':
    main()
    test_word_validation()