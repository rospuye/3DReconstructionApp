from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='test_video.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))

if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

    # # get the (largest) contour
    # contours = cv.findContours(fgMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # contours = contours[0] if len(contours) == 2 else contours[1]
    # # big_contour = max(contours, key=cv2.contourArea)

    # # draw white filled contour on black background
    # result = np.zeros_like(fgMask)
    # cv.drawContours(result, contours, 0, (255,255,255), cv.FILLED)

    window1 = 'Frame'
    window2 = 'FG Mask'
    cv.namedWindow(window1, cv.WINDOW_NORMAL)
    cv.namedWindow(window2, cv.WINDOW_NORMAL)
    cv.resizeWindow(window1, 300, 700)
    cv.resizeWindow(window2, 300, 700)
    
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

