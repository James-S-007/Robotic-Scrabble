import RPi.GPIO

GPIO.setmode(GPIO.BOARD)

# mux select pins, DCBA
mux_selectA = 
mux_selectB = 
mux_selectC = 
mux_selectD = 

# Hall effect row pins
hall_effect1 = 
hall_effect2 = 
hall_effect3 = 
hall_effect4 = 
hall_effect5 = 
hall_effect6 = 
hall_effect7 = 
hall_effect8 = 
hall_effect9 = 
hall_effect10 = 
hall_effect11 = 
hall_effect12 = 
hall_effect13 = 
hall_effect14 = 
hall_effect15 = 

# GPIO setup of mux select lines
GPIO.setup(mux_selectA, GPIO.IN)
GPIO.setup(mux_selectB, GPIO.IN)
GPIO.setup(mux_selectC, GPIO.IN)
GPIO.setup(mux_selectD, GPIO.IN)

# GPIO setup of Hall effect lines
GPIO.setup(hall_effect1, GPIO.OUT)
GPIO.setup(hall_effect2, GPIO.OUT)
GPIO.setup(hall_effect3, GPIO.OUT)
GPIO.setup(hall_effect4, GPIO.OUT)
GPIO.setup(hall_effect5, GPIO.OUT)
GPIO.setup(hall_effect6, GPIO.OUT)
GPIO.setup(hall_effect7, GPIO.OUT)
GPIO.setup(hall_effect8, GPIO.OUT)
GPIO.setup(hall_effect9, GPIO.OUT)
GPIO.setup(hall_effect10, GPIO.OUT)
GPIO.setup(hall_effect11, GPIO.OUT)
GPIO.setup(hall_effect12, GPIO.OUT)
GPIO.setup(hall_effect13, GPIO.OUT)
GPIO.setup(hall_effect14, GPIO.OUT)
GPIO.setup(hall_effect15, GPIO.OUT)

# TODO(James): See if can do cleaner with channel list
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/