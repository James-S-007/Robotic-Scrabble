import os.path
from pprint import pprint

import ai as AI
from Board import Board
from GameRules import GameRules


# things to test
    # word validation
    # word generation from set of letters
    # finding words from 

def main():
    game_rules = GameRules(os.path.join(os.path.dirname(__file__), 'dictionary.txt'))
    board = Board()
    board.import_board(os.path.join(os.path.dirname(__file__), 'board.csv'))  # TODO(James): import board.csv file
    test_word_validation(game_rules)
    test_word_generation(board, game_rules)


# Test Functions
def test_word_validation(game_rules):
    print('Starting word validation tests...')
    output_format(game_rules.validate_word('hello'), True)
    output_format(game_rules.validate_word('helloe'), False)
    output_format(game_rules.validate_word('tertiary'), True)
    output_format(game_rules.validate_word('cup'), True)

def test_word_generation(board, game_rules):
    rack = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    new_board = AI.make_best_move(board.board, rack, game_rules.dictionary)
    return


# Output Formatting
def output_format(result, expected_result):
    print(f'{"PASS" if result == expected_result else "FAIL"}\t\tTest Result: {result}\tExpected Result: {expected_result}')


if __name__ == '__main__':
    main()
