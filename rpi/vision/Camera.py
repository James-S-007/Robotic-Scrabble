from pyzbar import pyzbar
import cv2
import numpy as np

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
        self.mtx = np.array([[1078.88719, 0.00000000, 969.100204], \
                    [0.00000000, 1079.16746, 552.814241], \
                    [0.00000000, 0.00000000, 1.00000000]], dtype='float64')
        self.dist = np.array([-0.40432475, 0.1816134, -0.00207898, 0.00111414, -0.03938178], dtype='float64')
        self.roi = (866, 223, 740, 670)
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

    def capture_image(self, show_img=False):
        cap_num = 0
        while True:
            ret, image = self.cap.read()
            if show_img:
                dst = cv2.undistort(image, self.mtx, self.dist, None, self.new_camera_mtx)
                cv2.imshow('Imagetest', dst)
            k = cv2.waitKey(1)
            if k == ord(' '):
                cv2.imwrite(os.path.join(os.path.dirname(__file__), f'cv2_cap{cap_num}.jpg'), image)
                cap_num += 1
            if k == ord('q'):
                    break
            sleep(0.2)
    
if __name__ == '__main__':
    cam = Camera(0)
    cam.capture_image(show_img=True)
