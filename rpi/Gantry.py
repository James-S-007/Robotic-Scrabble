'''

'''
from random import randint

from Grbl.GrblStream import GrblStream
from Human import Human
from PathPlanner import PathPlanner
from scrabble.AI import AI
from Storage import Storage

from config import COM_PORT, ORIGIN

# testing imports
import os.path
from pprint import pprint
from scrabble.Board import Board
from scrabble.AI import AI
from scrabble.GameRules import GameRules

class Gantry:
    def __init__(self, board, human_rack, ai_rack):
        # pin setup on RPi & Serial connection w/ Arduino
        self.offsets = {'board': (3, 3), 'ai_rack': (19, 7), 'ai_cam': (18, 15), 'human_rack': (1, 7), 'storage1': (3, 0), 'storage2': (3, 19)}
        self.in2mm = 25.4
        self.storage1 = Storage(rows=15, cols=1)
        self.storage2 = Storage(rows=15, cols=1)
        self.planner = PathPlanner(board, human_rack, ai_rack, self.storage1, self.storage2, self.offsets)
        self.grbl_stream = GrblStream(COM_PORT)

    # base move pieces from start to end w/ path-planning
    def move(self, start, end):
        grid_moves = self.planner.simplify_path(self.planner.astar(start, end))
        print(f'Grid Space Moves: {grid_moves}')
        # fix axes: gantry <---> planner
        #           x <---> y
        #           y <---> -x
        for i in range(0, len(grid_moves)):
            grid_moves[i] = (grid_moves[i][1], (len(self.planner.grid) - 1) - grid_moves[i][0])

        absolute_moves = self.grid_pos_to_absolute_pos(grid_moves)
        print(f'Absolute Space Moves: {absolute_moves}')
        self.grbl_stream.gen_and_stream(absolute_moves)
        self.planner.update_global_grid()


    def grid_pos_to_absolute_pos(self, grid_moves):
        absolute_moves = [(ORIGIN[0] + move[0]*self.in2mm, ORIGIN[1] + move[1]*self.in2mm) for move in grid_moves]
        return absolute_moves


    def rand_sample_storage(self):
        storage = randint(1, 2)
        idx = None
        if storage == 1:
            idx = self.storage1.generate_letter()
        elif storage == 2:
            idx = self.storage2.generate_letter()
        # TODO(James): What to do if one storage bin runs out? Probably won't get that far but oh well
        return storage, idx


    # Player: Human or AI type
        # Human --> move pieces to static location on board near rack
        # AI --> move pieces to camera, scan, move to specific rack index
    def distribute_letters(self, player, num_letters):
        if type(player) is AI:
            for i in range(0, num_letters):
                storage, idx = self.rand_sample_storage()
                offset = self.offsets['storage1'] if storage == 1 else self.offsets['storage2']
                self.move((idx[0] + offset[0], idx[1] + offset[1]), self.offsets['ai_cam'])
                # find rack_idx
                rack_idx = player.rack.index(None)
                player.record_letter(rack_idx)
                self.move(self.offsets['ai_cam'], (rack_idx[0] + self.offsets['ai_rack'][0], rack_idx[1] + self.offsets['ai_rack'][1]))
        elif type(player) is Human:
            for i in range(0, num_letters):
                storage, idx = self.rand_sample_storage()
                offset = self.offsets['storage1'] if storage == 1 else self.offsets['storage2']
                self.move((idx[0] + offset[0], idx[1] + offset[1]), self.offsets['human_rack'])
        else:
            print('Err: Invalid player type')
            return


    # Plays AI move
    # take in rack_idx --> board_location
    def play_letters(self, player, move):
        if type(player) is AI:
            for rack_idx, board_idx in move.items():
                rack_offset = self.offsets['ai_rack']
                board_offset = self.offsets['board']
                self.move((rack_offset[0], rack_idx + rack_offset[1]), (board_idx[0] + board_offset[0], board_idx[1] + board_offset[1]))
        else:
            print('Err: Invalid player type')
            return
        

# test
if __name__ == '__main__':
    board = Board()
    board.import_board(os.path.join(os.path.dirname(__file__), 'scrabble', 'board.csv'))
    human_rack = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    ai = AI()
    ai.rack = ['h', 'i', 'j', 'k', 'l', 'm', 'n']
    game_rules = GameRules(dictionary=os.path.join(os.path.dirname(__file__), 'scrabble', 'dictionary.txt'))
    gantry = Gantry(board, human_rack, ai.rack)
    print('Current Grid')
    pprint(gantry.planner.grid)
    ai_move = ai.generate_move(board, game_rules)
    print('AI Move')
    pprint(ai_move)
    gantry.play_letters(ai, ai_move['moves'])
    gantry.distribute_letters(ai, ai.rack.count(None))
    # gantry.move((20, 0), (17, 13))
    