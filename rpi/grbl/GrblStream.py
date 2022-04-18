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
                f.write(f'G21 G90 X{round(cmd[0], 3)} Y{round(cmd[1], 3)} F5000\n')
            

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