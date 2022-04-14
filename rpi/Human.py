'''

'''

# import RPi.GPIO
from copy import deepcopy
from time import sleep

import halleffect

class Human:

    def __init__(self):
        self.rack = [None]*7
        self.score = 0

    # records where human player places letters
    def record_move(self, board, end_turn_pb, cam):
        move = {}
        hall_effect_arr = deepcopy(board.board)
        prev_letter = curr_letter = None
        while not GPIO.input(end_turn_pb):
            prev_letter = curr_letter
            curr_letter = None
            while not curr_letter:
                curr_letter = cam.check_letter()
                sleep(.05)
            if move:   # not first turn, check where prev letter was placed
                new_sensors = halleffect.check_new_sensors(hall_effect_arr)
                if not new_sensors or len(new_sensors) > 1:
                    print('Err: No new tile detected or multiple new tiles detected')  # TODO(James): What to do here
                move[prev_letter] = new_sensors[0]
                for sensor in new_sensors:
                    hall_effect_arr[sensor[0]][sensor[1]] = 1  # update hall_effect_arr
        new_sensors = halleffect.check_new_sensors(hall_effect_arr)
        if not new_sensors or len(new_sensors) > 1:
            print('Err: No new tile detected or multiple new tiles detected')  # TODO(James): What to do here
        move[curr_letter] = new_sensors[0]
        for sensor in new_sensors:
            hall_effect_arr[sensor[0]][sensor[1]] = 1  # update hall_effect_arr
        return move

    def find_words_played(self, board, move):
        temp_board = deepcopy(board.board)
        words = {}  # dict: {(root_x, root_y, axis (0 or 1)): word, ...}
        for letter, location in move.items():
            temp_board[location[0]][location[1]] = letter  # update temp board (need old in case move invalid)
        offsets = {(0, 1): 0, (0, -1): 0, (1, 0): 1, (-1, 0): 1}
        for letter, location in move.items():
            for offset, axis in offsets.items():
                root, word = self.find_word([location[0]+offset[0], location[1]+offset[1]], axis, temp_board)
                if word and root not in words:
                    words[root] = word
        return words

        
    def find_word(self, location, axis, board_arr):
        if location[0] < 0 or location[0] > 14 or location[1] < 0 or location[1] > 14 or board_arr[location[0]][location[1]] == '-':
            return None, None
        const_idx = location[axis]
        curr_idx = location[1 - axis]
        word = ''
        root = None
        if axis == 0:
            while curr_idx > 0 and board_arr[const_idx][curr_idx - 1] != '-':  # TODO(James): Input stuff to deal with side of boared
                curr_idx -= 1
            root = (const_idx, curr_idx, axis)
            while curr_idx <= 14 and board_arr[const_idx][curr_idx] != '-':
                word += board_arr[const_idx][curr_idx]
                curr_idx += 1
        elif axis == 1:
            while curr_idx > 0 and board_arr[curr_idx - 1][const_idx] != '-':
                curr_idx -= 1
            root = (curr_idx, const_idx, axis)
            while curr_idx <= 14 and board_arr[curr_idx][const_idx] != '-':
                word += board_arr[curr_idx][const_idx]
                curr_idx += 1
        return root, word


    # records move being made, scores word and updates board
    # returns --> False if word placed invalid, True if successful turn
    def make_move(self, board, game_rules, end_turn_pb, cam):
        move = self.record_move(board, end_turn_pb, cam)
        words_played = self.find_words_played(self, board, move)
        turn_score = 0
        for _, word in words_played.items():
            if game_rules.validate_word(word):
                turn_score += game_rules.score_word(word)
            else:
                print(f'Err: {word} is not a valid word. Please remove all pieces placed this turn and try again')
                return False
        # update board for real this time
        for letter, location in move.items():
            board.board[location[0]][location[1]] = letter
        self.score += turn_score
        return True
        # TODO(James): where to put distribute pieces?
