from pyzbar import pyzbar
import cv2

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
