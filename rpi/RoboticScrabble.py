import os.path
import sys.exit
from random import randint

from Gantry import Gantry
from Human import Human
from scrabble.AI import AI
from scrabble.GameRules import GameRules
from scrabble.Board import Board

# initialize objects
board = Board(n=15)
human = Human(cam_num=1)
ai = AI(cam_num=2)
gantry = Gantry(board, human.rack, ai.rack)
game_rules = GameRules(dictionary=os.path.join(os.path.dirname(__file__), 'scrabble', 'dictionary.txt'))
# TODO(James): insert some player input stuff somewhere (mainly end turn pb)
end_turn_pb = 

# pick starting player and output to LCD
curr_player = randint(0, 1)  # Human: 0, AI: 1, to toggle player  1 - curr_player
while True:
    if curr_player == 0:  # Human turn
        words = []
        score = 0
        while not words:
            words, score = human.make_move(board, game_rules, end_turn_pb):
        # TODO(James): Output words made and score to LCD     
        # find number of pieces to dist
        gantry.distribute_letters(human, human.rack.count(None))
    elif curr_player == 1:  # AI turn
        ai_move = ai.generate_move(board, game_rules)
        gantry.play_letters(ai, ai_move['moves'])
        gantry.distribute_letters(ai, ai.rack.count(None))
        # TODO(James): output words made and score to LCD
    else:
        print('Err: Invalid player number exiting...')
        sys.exit()
    curr_player = 1 - curr_player  # toggle current player after turn
        
# TODO(James): Some results output?