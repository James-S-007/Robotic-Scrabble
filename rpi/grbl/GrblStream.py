import serial
from time import sleep
import os.path

# SERVO: M3 S1 --> Raise
#        M3 S3500 --> Lower

class GrblStream:
    def __init__(self, com_port):
        self.s = serial.Serial(com_port, 115200)
        self.s.write(str.encode("\r\n\r\n"))  # wake up grbl
        self.gcode_path = os.path.join(os.path.dirname(__file__), 'grbl.gcode')
        print('Waking up Grbl...')
        sleep(2)
        self.s.flushInput()
        self.home()
        print('Grbl initalization complete')
        

    def __del__(self):
        self.s.close()

    # cmds = [(x, y), (x, y), ...]
    def gen_gcode(self, cmds):
        with open(self.gcode_path, 'w') as f:
            f.write('$X\n')
            # f.write(f'G21 G90 X35 Y30 F5000\n')
            # TODO(James): Make this cleaner, quick fix for now to implement servo
            count = 0
            f.write('M3 S3500\n')
            for cmd in cmds:
                f.write(f'G21 G90 X{round(cmd[0], 3)} Y{round(cmd[1], 3)} F5000\n')
                if count == 0:
                    f.write('M3 S1\n')  # raise servo after reaching home position
            f.write('M3 S3500\n')  # finally lower servo at end
                

            

    def send_gcode(self):
        # Stream g-code to grbl
        with open(self.gcode_path, 'r') as f:
            for line in f:
                l = line.strip() # Strip all EOL characters for consistency
                print(f'Sending: {l}')
                self.s.write(str.encode(l + '\n')) # Send g-code block to grbl
                grbl_out = self.s.readline() # Wait for grbl response with carriage return
                print (f'Response: {grbl_out.strip()}')

    def home(self):
        with open(self.gcode_path, 'w') as f:
            f.write('M3 S3500\n')  # initially lower magnet
            f.write('$H\n')
            f.write(f'G21 G90 X50 Y50 F5000\n')

        self.send_gcode()
        sleep(5)

    def gen_and_stream(self, cmds):
        self.gen_gcode(cmds)
        self.send_gcode()
        sleep(10)

# test
if __name__ == '__main__':
    grbl = GrblStream('COM5')
    grbl.gen_and_stream(cmds=[(200, 200), (150, 100), (100, 150), (100, 100)])