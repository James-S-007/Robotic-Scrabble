'''

'''
from random import randint

from robotic_scrabble.AI import AI
from Human import Human
from PathPlanner import PathPlanner
from Storage import Storage

class Gantry:
    def __init__(self, board):
        # pin setup on RPi & Serial connection w/ Arduino
        self.offsets = {'ai_rack': [, ], 'ai_cam': [, ], 'human_rack': [, ], 'storage1': [, ], 'storage2', [, ]}
        self.planner = PathPlanner(board)
        self.storage1 = Storage()
        self.storage2 = Storage()

    # base move pieces from start to end w/ path-planning
    def move(self, start, end):
        return self.planner.simplify_path(self.planner.astar(start, end))

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
        # Human --> move pieces to static location on board
        # AI --> move pices to camera, scan, move to specific rack index
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
            # gen all indexes from storage
            # for storage_location in group
                # move(start, static_location)
            return
        else:
            print('Err: Invalid player type')
            return

    # Plays AI move
    # take in rack_idx --> board_location
    def play_letters(self, move):
        return
        