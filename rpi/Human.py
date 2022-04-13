'''

'''

import RPi.GPIO
from time import sleep

import halleffect

class Human:

    def __init__(self):
        self.rack = [None]*7
        self.score = 0

    # records where human player places letters
    def record_move(self, board, end_turn_pb, cam):
        move = {}
        hall_effect_arr = board.board.copy()
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

    # records move being made, scores word and updates board
    def make_move(self, board, game_rules, end_turn_pb, cam):
        move = self.record_move(board, end_turn_pb, cam)
        