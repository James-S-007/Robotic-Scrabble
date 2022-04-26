from pyzbar import pyzbar
import cv2
import numpy as np

import os.path
from time import sleep
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from vision.scrabbleCV import getGameBoards

# TODO(James):
    # https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
    # https://github.com/tizianofiorenzani/how_do_drones_work/blob/master/opencv/cameracalib.py

# To modify camera parameters: v4l2-ctl -d /dev/video0 --list-ctrls-menus
# Camera height above board: 26in

CAM_FILE_NAME = 'robotic_scrabble_game_util.jpg'

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = cv2.VideoCapture(cam_num)
        if not self.cap.isOpened():
            print('Err: Cannot Open Camera')
            self.valid = False
        else:
            self.valid = True
        self.mtx = np.array([[1078.88719, 0.00000000, 969.100204], \
                    [0.00000000, 1079.16746, 552.814241], \
                    [0.00000000, 0.00000000, 1.00000000]], dtype='float64')
        self.dist = np.array([-0.40432475, 0.1816134, -0.00207898, 0.00111414, -0.03938178], dtype='float64')
        self.roi = (866, 223, 740, 670)
        self.x, self.y, self.w, self.h = self.roi
        self.new_camera_mtx = np.array([[415.86682129, 0.0000000000, 1239.7650000], \
                                [0.000000000, 669.40087891, 565.55338968], \
                                [0.000000000, 0.0000000000, 1.0000000000]], dtype='float64')
        # self.new_camera_mtx = cv2.UMat(self.new_camera_mtx)

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

    def stream_image(self, show_img=False):
        cap_num = 0
        while True:
            ret, image = self.cap.read()
            if not ret:
                print('Camera disconnected, exiting...')
                return False
            dst = cv2.undistort(image, self.mtx, self.dist, None, self.new_camera_mtx)
            dst = dst[self.y:self.y+self.h, self.x:self.x+self.w]  # crop
            if show_img:
                # cv2.imshow('Imagetest', dst)
                cv2.imshow('Imagetest', image)
            k = cv2.waitKey(1)
            if k == ord(' '):
                # cv2.imwrite(os.path.join(os.path.dirname(__file__), f'cv2_cap{cap_num}.jpg'), image)
                cv2.imwrite(os.path.join(os.path.dirname(__file__), f'cv2_cap{cap_num}.jpg'), dst)
                cap_num += 1
            if k == ord('q'):
                    break

    def save_image(self):
        ret, image = self.cap.read()
        if not ret:
            print('Camera disconnected, exiting...')
            return None
        dst = cv2.undistort(image, self.mtx, self.dist, None, self.new_camera_mtx)
        dst = dst[self.y:self.y+self.h, self.x:self.x+self.w]  # crop
        img_path = os.path.join(os.path.dirname(__file__), CAM_FILE_NAME)
        cv2.imwrite(img_path, dst)
        # cv2.imwrite(img_path, image)
        

    def output_rack_and_board(self):
        self.save_image()
        return getGameBoards(os.path.join(os.path.dirname(__file__), CAM_FILE_NAME))

        
    
if __name__ == '__main__':
    cam = Camera(1)
    cam.stream_image(show_img=True)
