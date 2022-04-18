import os.path
from pprint import pprint

from AI import AI
from Board import Board
from GameRules import GameRules


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
    move = ai.generate_move(board, game_rules)
    print('AI Move:')
    pprint(move)
    output_format(ai.rack, ['a', None, 'c', 'd', None, 'f', 'g'])
    print('New board:')
    pprint(board.board)
    ai.rack = ['h', 'i', 'j', 'k', 'l', 'm', 'n']
    pprint(f'New Rack: {ai.rack}, New Score: {ai.score}')
    board.import_board(os.path.join(os.path.dirname(__file__), 'board.csv'))  # reset board
    move = ai.generate_move(board, game_rules)
    print('AI Move:')
    pprint(move)
    output_format(ai.rack, [None, None, 'j', None, 'l', 'm', 'n'])
    print('New board:')
    pprint(board.board)


# Output Formatting
def output_format(result, expected_result):
    print(f'{"PASS" if result == expected_result else "FAIL"}\t\tTest Result: {result}\tExpected Result: {expected_result}')


if __name__ == '__main__':
    main()
