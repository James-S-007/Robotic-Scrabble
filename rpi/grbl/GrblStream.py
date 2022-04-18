#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
Provided as an illustration of the basic communication interface
for grbl. When grbl has finished parsing the g-code block, it will
return an 'ok' or 'error' response. When the planner buffer is full,
grbl will not send a response until the planner buffer clears space.
G02/03 arcs are special exceptions, where they inject short line 
segments directly into the planner. So there may not be a response 
from grbl for the duration of the arc.
---------------------
The MIT License (MIT)
Copyright (c) 2012 Sungeun K. Jeon
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
---------------------
"""

import serial
from time import sleep
import os.path

class GrblStream:
    def __init__(self, com_port):
        self.s = serial.Serial(com_port, 115200)
        self.s.write(str.encode("\r\n\r\n"))  # wake up grbl
        self.gcode_path = os.path.join(os.path.dirname(__file__), 'grbl.gcode')
        print('Waking up Grbl...')
        sleep(2)
        self.s.flushInput()
        print('Grbl initalization complete')
        

    def __del__(self):
        self.s.close()

    # cmds = [(x, y), (x, y), ...]
    def gen_gcode(self, cmds):
        with open(self.gcode_path, 'w') as f:
            f.write('$H\n')
            for cmd in cmds:
                f.write(f'G21 G90 X{cmd[0]} Y{cmd[1]} F5000\n')
            

    def send_gcode(self):
        # Stream g-code to grbl
        with open(self.gcode_path, 'r') as f:
            for line in f:
                l = line.strip() # Strip all EOL characters for consistency
                print(f'Sending: {l}')
                self.s.write(str.encode(l + '\n')) # Send g-code block to grbl
                grbl_out = self.s.readline() # Wait for grbl response with carriage return
                print (f'Response: {grbl_out.strip()}')

    def gen_and_stream(self, cmds):
        self.gen_gcode(cmds)
        self.send_gcode()

# test
if __name__ == '__main__':
    grbl = GrblStream('COM5')
    grbl.gen_and_stream(cmds=[(200, 200), (150, 100), (100, 150), (100, 100)])