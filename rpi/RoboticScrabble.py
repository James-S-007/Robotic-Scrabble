import os.path
from random import randint

from Gantry import Gantry
from Human import Human
from scrabble.AI import AI
from scrabble.GameRules import GameRules
from scrabble.Board import Board
from vision import Camera
from gui.gui import FullScreenApp
import tkinter as tk

from time import sleep

# initialize objects
board = Board(n=15)
human = Human()
ai = AI(cam_num=2)
gantry = Gantry(board, human.rack, ai.rack)
game_rules = GameRules(dictionary=os.path.join(os.path.dirname(__file__), 'scrabble', 'dictionary.txt'))
# camera = Camera(cam_num=1)


# pick starting player and output to LCD
curr_player = randint(0, 1)  # Human: 0, AI: 1, to toggle player  1 - curr_player

# Gui button callbacks
def end_turn_cb():
    global board
    global ai
    global gantry
    board.import_board(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_game_board.csv'))  # update board
    ai.import_rack(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_ai_rack.csv'))  # update rack
        # ai.update_board(board, new_board)
        # ai.update_rack(new_rack)
    ai_move = ai.generate_move(board, game_rules)
    print(f'AI Move: {ai_move}')
    gantry.play_letters(ai, ai_move['moves'])
        


def end_game_cb():
    global curr_player
    curr_player = -1
    exit()

root=tk.Tk()
app=FullScreenApp(root, button_endturn_cb=end_turn_cb, button_endgame_cb=end_game_cb)
root.mainloop()

# board.import_board(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_game_board.csv'))  # update board
# ai.import_rack(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_ai_rack.csv'))  # update rack
# ai_move = ai.generate_move(board, game_rules)


'''
print(f'Starting player: {"Human" if 0 else "AI"}')
while True:
    if curr_player == 0:  # Human turn
        # words = []
        # score = 0
        # while not words:
            
            # words, score = human.make_move(board, game_rules, end_turn_pb):
        # print(f'Words Made: {words}\nScore:{score}')
        sleep(0.2)
        # find number of pieces to dist
        # gantry.distribute_letters(human, human.rack.count(None))
    elif curr_player == 1:  # AI turn
        # new_board, new_rack = camera.output_rack_and_board()
        board.import_board(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_game_board.csv'))  # update board
        ai.import_rack(os.path.join(os.path.dirname(__file__), 'scrabble', 'scrabble_ai_rack.csv'))  # update rack
        # ai.update_board(board, new_board)
        # ai.update_rack(new_rack)
        ai_move = ai.generate_move(board, game_rules)
        gantry.play_letters(ai, ai_move['moves'])
        curr_player = 0  # human turn
        # gantry.distribute_letters(ai, ai.rack.count(None))
        # TODO(James): output words made and score to LCD
    else:
        # print('Err: Invalid player number exiting...')
        print('Game over!')
        break
    # curr_player = 1 - curr_player  # toggle current player after turn
        
# TODO(James): Some results output?
'''