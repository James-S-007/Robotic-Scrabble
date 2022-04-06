from pyzbar import pyzbar
import cv2

def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # return letter barcode found
        return(obj.data)

def checkLetter(camNum, check):
    cap = cv2.VideoCapture(camNum)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while check:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # decode barcode
        frame = decode(frame)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
