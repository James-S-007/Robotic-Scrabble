# Based on Sudoko tutorial: https://pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/#pyis-cta-modal

# import the necessary packages
from pydoc import doc
from perspective import four_point_transform
from skimage.segmentation import clear_border 
import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras.datasets import mnist
import pytesseract
from PIL import Image

debug = True

def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    # return the actual contours array
    return cnts


def extract_letter(cell, debug=False):

    # apply automatic thresholding to the cell and then clear any
    # connected borders that touch the border of the cells
    thresh = cv2.threshold(cell, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)

    # check to see if we are visualizing the cell thresholding step
    if debug:
        cv2.imshow("Cell Thresh", thresh)
        cv2.waitKey(0)

    # find contours in the thresholded cell
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)

    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        return None

    # otherwise, find the largest contour in the cell and create a
    # mask for the contour
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # compute the percentage of masked pixels relative to the total
    # area of the image
    (h, w) = thresh.shape
    percentFilled = cv2.countNonZero(mask) / float(w * h)

    # if less than 3% of the mask is filled then we are looking at
    # noise and can safely ignore the contour
    if percentFilled < 0.05:
        return None
    # apply the mask to the thresholded cell
    letter = cv2.bitwise_and(thresh, thresh, mask=mask)
    # check to see if we should visualize the masking step
    if debug:
        cv2.imshow("letter", letter)
        cv2.waitKey(0)
    # return the letter to the calling function
    return letter

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


if __name__ == "__main__":
    image = cv2.imread( os.path.dirname(os.path.realpath(__file__)) + '/images/highResScrabble.jpg')
    
    # Rotate image
    image = rotate_image(image,92)

    cv2.imshow("Gameboard Image",image)
    cv2.waitKey(0)

    # find the board in the image and then
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply adaptive thresholding and then invert the threshold map
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    #cv2.imshow("Gray Game board Image",thresh)
    #cv2.waitKey(0)

    mainBoardCnt = np.array([[[92,487]],[[646,477]],[[665,129]],[[88,134]]])

    playerCnt = np.array([[[241,530]],[[500,528]],[[500,506]],[[239,511]]])

    if False:
        # draw the contour of the mainBoard on the image and then display
        # it to our screen for visualization/debugging purposes
        output = image.copy()
        cv2.drawContours(output, [mainBoardCnt], -1, (0, 255, 0), 2)
        cv2.imshow("mainBoard Outline", output)
        cv2.waitKey(0)

    if True:
        # Draw contour of the playerTiles on the image and display it
        output = image.copy()
        cv2.drawContours(output, [playerCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Player Tiles Outline", output)
        cv2.waitKey(0)

    mainBoardImage = four_point_transform(gray, mainBoardCnt.reshape(4, 2))

    playerBoard = four_point_transform(gray, playerCnt.reshape(4, 2))
    
    # initialize our 15x15 Scrabble board
    mainBoard = np.zeros((15, 15), dtype=str)

    # initialize our 1x7 player board
    playerTiles = np.zeros((1,7),dtype=str)

    if False:
        cv2.imshow("Cropped Mainboard",mainBoardImage)
        cv2.waitKey(0)
    
    if True:
        cv2.imshow("Cropped Player Board",playerBoard)
        cv2.waitKey(0)

    stepX = mainBoardImage.shape[1] / 15.0
    stepY = mainBoardImage.shape[0] / 15.0


    # Load model from https://github.com/shivamgupta7/OCR-Handwriting-Recognition
    model = tf.keras.models.load_model(os.path.dirname(os.path.realpath(__file__)) + '/model/handwriting.model')

    # define the list of label names
    labelNames = "0123456789"
    labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    labelNames = [l for l in labelNames]

    numbers = "0123456789"
    numbers = [n for n in labelNames]

    i = 0
    # loop over the grid locations
    for y in range(0, 15):
        for x in range(0, 15): 
            # current cell 
            startX = int(x * stepX)
            startY = int(y * stepY)
            endX = int((x + 1) * stepX)
            endY = int((y + 1) * stepY)

            # crop the cell from the warped transform image and then
            # extract the letter from the cell
            cell = mainBoardImage[startY:endY, startX:endX]

            #cv2.imshow("Cell",cell )
            #cv2.waitKey(0)
            letter = extract_letter(cell, False)

            # verify that the letter is not empty
            if letter is not None:
                # resize the cell to 28x28 pixels and then prepare the
                # cell for classification
                roi = cv2.resize(letter, (32, 32))
                roi = roi.astype("float") / 255.0
                cv2.imshow("letter",roi)
                cv2.waitKey(0)
                roi = tf.keras.utils.img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                # classify the letter and update the Scrabble board with the
                # prediction
                pred = model.predict(roi)
                #print(pred)
                #indices = np.argsort(pred, axis=-1, kind='quicksort', order=None)
                #print(indices)
                #i = indices[0][0]
                #prob = pred[0][0]
                i = np.argmax(pred)
                print("Index",i)
                indices = np.argsort(pred, axis=-1, kind='quicksort', order=None)
                print(indices)
                label = labelNames[i]

                # Make sure we aren't predicting a number
                """ j = 0
                w = -2
                while (j < 10):
                    if(label == numbers[j]):
                        print("Number was predicted, using different prediction")
                        j = 0
                        i = indices[0][w]
                        #prob = pred[w]
                        label = labelNames[w]
                        w = w - 1
                    else:
                        j = j + 1 """
                
                print("Prediction: ",label)
                #print("Probability: ",prob)
                mainBoard[y, x] = label
            else:
                mainBoard[y,x] = '-'

    stepX = playerBoard.shape[1] / 7.0
    stepY = mainBoardImage.shape[0] / 15.0

    # Classify Letters in Player board
    """ for x in range(0, 7): 
        # current cell 
        startX = int(x * stepX)
        startY = 0
        endX = int((x + 1) * stepX)  
        endY = int(stepY)

        # crop the cell from the warped transform image and then
        # extract the letter from the cell
        cell = playerBoard[startY:endY, startX:endX]

        cv2.imshow("Cell",cell )
        cv2.waitKey(0)
        letter = extract_letter(cell, False)

        # verify that the letter is not empty
        if letter is not None:
            # resize the cell to 28x28 pixels and then prepare the
            # cell for classification
            roi = cv2.resize(letter, (32, 32))
            roi = roi.astype("float") / 255.0
            cv2.imshow("letter",roi)
            cv2.waitKey(0)
            roi = tf.keras.utils.img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            # classify the letter and update the Scrabble board with the
            # prediction
            pred = model.predict(roi)
            np.argsort(pred, axis=-1, kind='quicksort', order=None)
            i = pred[0][0]
            #prob = pred[0][0]
            label = labelNames[i]
            
            # Make sure we aren't predicting a number
            j = 0
            w = 1
            while (j < 10):
                if(label == numbers[j]):
                    print("Number was predicted, using different prediction")
                    j = 0
                    w = w + 1
                    i = pred[0][w]
                    prob = pred[w]
                    label = labelNames[w]
                else:
                    j = j + 1
            

            print("Prediction: ",label)
            ##print("Probability: ",prob)
            playerTiles[0,x] = label
        else:
            playerTiles[0,x] = '-' """
        
    print(mainBoard)
    #print(playerTiles)


