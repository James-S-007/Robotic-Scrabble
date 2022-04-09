import os.path
from pprint import pprint

from AI import AI
from Board import Board
from GameRules import GameRules


# things to test
    # word validation
    # word generation from set of letters
    # finding words from 

def main():
    game_rules = GameRules(os.path.join(os.path.dirname(__file__), 'dictionary.txt'))
    board = Board()
    board.import_board(os.path.join(os.path.dirname(__file__), 'board.csv'))
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
    ai = AI()
    ai.rack = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    move = ai.ai_make_move(board, game_rules)
    print('AI Move:')
    pprint(move)
    print('New board:')
    pprint(board.board)
    ai.update_state({0: 'h', 1: 'i', 2: 'j', 3: 'k', 4: 'l', 5: 'm', 6: 'n'}, move['score'])
    pprint(f'New Rack: {ai.rack}, New Score: {ai.score}')
    board.import_board(os.path.join(os.path.dirname(__file__), 'board.csv'))  # reset board
    move = ai.ai_make_move(board, game_rules)
    print('AI Move:')
    pprint(move)
    print('New board:')
    pprint(board.board)


# Output Formatting
def output_format(result, expected_result):
    print(f'{"PASS" if result == expected_result else "FAIL"}\t\tTest Result: {result}\tExpected Result: {expected_result}')


if __name__ == '__main__':
    main()
