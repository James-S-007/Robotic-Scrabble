import os.path

from GameRules import GameRules


# things to test
    # word validation
    # word generation from set of letters
    # finding words from 

game_rules = GameRules(os.path.join(os.path.dirname(__file__), 'dictionary.txt'))

print(game_rules.validate_word('hello'))
print(game_rules.validate_word('helloe'))