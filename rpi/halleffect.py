# import RPi.GPIO

# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

# mux select pins, DCBA
mux_selectA = 0
mux_selectB = 0
mux_selectC = 0
mux_selectD = 0
mux_selects = [mux_selectD, mux_selectC, mux_selectB, mux_selectA]

# Hall effect row pins
hall_effect0 = 0
hall_effect1 = 0
hall_effect2 = 0
hall_effect3 = 0
hall_effect4 = 0
hall_effect5 = 0
hall_effect6 = 0
hall_effect7 = 0
hall_effect8 = 0
hall_effect9 = 0
hall_effect10 = 0
hall_effect11 = 0
hall_effect12 = 0
hall_effect13 = 0
hall_effect14 = 0
hall_effects = [hall_effect0, hall_effect1, hall_effect2, hall_effect3, hall_effect4, hall_effect5, hall_effect6, hall_effect7,\
                hall_effect8, hall_effect9, hall_effect10, hall_effect11, hall_effect12, hall_effect13, hall_effect14]

# GPIO setup of mux select lines and hall effect lines
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(mux_selects, GPIO.IN)
# GPIO.setup(hall_effects, GPIO.OUT)

# column is an integer [0,14]
def select_hall_effect(column):
    if column == 0:
        mux_selects = [0,0,0,0]
    elif column == 1:
        mux_selects = [0,0,0,1]
    elif column == 2:
        mux_selects = [0,0,1,0]
    elif column == 3:
        mux_selects = [0,0,1,1]
    elif column == 4:
        mux_selects = [0,1,0,0]
    elif column == 5:
        mux_selects = [0,1,0,1]
    elif column == 6:
        mux_selects = [0,1,1,0]
    elif column == 7:
        mux_selects = [0,1,1,1]
    elif column == 8:
        mux_selects = [1,0,0,0]
    elif column == 9:
        mux_selects = [1,0,0,1]
    elif column == 10:
        mux_selects = [1,0,1,0]
    elif column == 11:
        mux_selects = [1,0,1,1]
    elif column == 12:
        mux_selects = [1,1,0,0]
    elif column == 13:
        mux_selects = [1,1,0,1]
    elif column == 14:
        mux_selects = [1,1,1,0]
    else:
        mux_selects = [0,0,0,0]
        print('Err: Invalid column selected for multiplexers, setting to 0 idx')


def read_all_sensors(hall_effect_arr):
    for i in range(0, len(hall_effects)):
        select_hall_effect(i)
        for j in range(0, len(hall_effects)):
            hall_effect_arr[j][i] = GPIO.input(hall_effects[j])

def check_new_sensors(prev_hall_effect_arr):
    new_sensors = []
    for i in range(0, len(hall_effects)):
        select_hall_effect(i)
        for j in range(0, len(hall_effects)):
            if GPIO.input(hall_effects[j]) != prev_hall_effect_arr[j][i]:
                new_sensors.append([j, i])
    return new_sensors

def get_tile_indices(hall_effect_arr):
    return [(ix,iy) for ix, row in enumerate(hall_effect_arr) for iy, i in enumerate(row) if i == 0]
