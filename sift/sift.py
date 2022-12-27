# import numpy as np
import cv2 as cv

img1 = cv.imread('santorini/1.png')
img2 = cv.imread('santorini/2.png')

images = [img1, img2]

for img in images:

    # resize image (only do this if it's too big)
    scale_percent = 20 # % of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    sift = cv.SIFT_create(nfeatures=500)
    kp, des = sift.detectAndCompute(gray, None) # keypoints, descriptors
    cv.drawKeypoints(img, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # show result
    title = 'sift result'
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    cv.resizeWindow(title, 800, 800)
    cv.imshow(title, img)
    cv.waitKey(-1)
