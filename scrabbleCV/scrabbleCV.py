# Based on Sudoko tutorial: https://pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/#pyis-cta-modal

# import the necessary packages
from perspective import four_point_transform
from skimage.segmentation import clear_border 
import numpy as np
import cv2
import os

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


def find_board(image, debug=False):

    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)

    # apply adaptive thresholding and then invert the threshold map
    thresh = cv2.adaptiveThreshold(blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # check to see if we are visualizing each step of the image
    # processing pipeline (in this case, thresholding)
    if debug:
        cv2.imshow("board Thresh", thresh)
        cv2.waitKey(0)

    # find contours in the thresholded image and sort them by size in
    # descending order
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # initialize a contour that corresponds to the board outline
    boardCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can
        # assume we have found the outline of the board
        if len(approx) == 4:
            boardCnt = approx
            break

    # if the board contour is empty then our script could not find
    # the outline of the Scrabble board so raise an error
    if boardCnt is None:
        raise Exception(("Could not find Scrabble Board outline. "
            "Try debugging your thresholding and contour steps."))
    # check to see if we are visualizing the outline of the detected
    # Sudoku board
    if debug:
        # draw the contour of the board on the image and then display
        # it to our screen for visualization/debugging purposes
        output = image.copy()
        cv2.drawContours(output, [boardCnt], -1, (0, 255, 0), 2)
        cv2.imshow("board Outline", output)
        cv2.waitKey(0)

    # apply a four point perspective transform to both the original
    # image and grayscale image to obtain a top-down bird's eye view
    # of the board
    board = four_point_transform(image, boardCnt.reshape(4, 2))
    warped = four_point_transform(gray, boardCnt.reshape(4, 2))
    # check to see if we are visualizing the perspective transform
    if debug:
        # show the output warped image (again, for debugging purposes)
        cv2.imshow("board Transform", board)
        cv2.waitKey(0)  
    # return a 2-tuple of board in both RGB and grayscale
    return (board, warped)

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
    if percentFilled < 0.03:
        return None
    # apply the mask to the thresholded cell
    letter = cv2.bitwise_and(thresh, thresh, mask=mask)
    # check to see if we should visualize the masking step
    if debug:
        cv2.imshow("letter", letter)
        cv2.waitKey(0)
    # return the letter to the calling function
    return letter

if __name__ == "__main__":
    image = cv2.imread( os.path.dirname(os.path.realpath(__file__)) + '/images/scrabbleBoardImage.jpg')

    # find the board in the image and then
    (boardImage, warped) = find_board(image, False)
    
    # initialize our 5x5 Scrabble board
    board = np.zeros((5, 6), dtype="int")

    cv2.imshow("Cropped",warped)
    cv2.waitKey(0)
    stepX = warped.shape[1] // 5
    stepY = warped.shape[0] // 5

    # initialize a list to store the (x, y)-coordinates of each cell
    # location
    cellLocs = []

    # loop over the grid locations
    for y in range(0, 5):
        # initialize the current list of cell locations
        row = []
        for x in range(0, 5): 
            # current cell 
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY
            # add the (x, y)-coordinates to our cell locations list
            row.append((startX, startY, endX, endY))

            # crop the cell from the warped transform image and then
            # extract the letter from the cell
            cell = warped[startY:endY, startX:endX]
            cv2.imshow("cell",cell )
            cv2.waitKey(0)
            letter = extract_letter(cell, False)
            # verify that the letter is not empty
            if letter is not None:
                # resize the cell to 28x28 pixels and then prepare the
                # cell for classification
                roi = cv2.resize(letter, (28, 28))
                roi = roi.astype("float") / 255.0
                cv2.imshow("letter",roi)
                cv2.waitKey(0)
                #roi = img_to_array(roi)
                #roi = np.expand_dims(roi, axis=0)
                # classify the letter and update the Sudoku board with the
                # prediction
                #pred = model.predict(roi).argmax(axis=1)[0] # TODO: Predict Letter...
                #board[y, x] = pred
        # add the row to our cell locations
        #cellLocs.append(row)


