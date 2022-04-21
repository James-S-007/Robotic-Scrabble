from pyzbar import pyzbar
import cv2

import os.path
from time import sleep

# To modify camera parameters: v4l2-ctl -d /dev/video0 --list-ctrls-menus
# Camera height above board: 26in

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = cv2.VideoCapture(cam_num)
        if not self.cap.isOpened():
            print('Err: Cannot Open Camera')
            self.valid = False
        else:
            self.valid = True

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()  

    def decode(self, image):
        # decodes all barcodes from an image
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            # return letter barcode found
            return(obj.data)

    def check_letter(self):
        ret, frame = self.cap.read()
        return self.decode(frame)

    def capture_image(self, show_img=False):
        cap_num = 0
        while True:
            ret, image = self.cap.read()
            if show_img:
                cv2.imshow('Imagetest', image)
            cv2.imwrite(os.path.join(os.path.dirname(__file__), f'cv2_cap{cap_num}.jpg'), image)
            cap_num += 1
            k = cv2.waitKey(1)
            if k != -1:
                    break
            sleep(0.2)
    
if __name__ == '__main__':
    cam = Camera(0)
    cam.capture_image()
