import cv2 as cv
import numpy as np

# duck = cv.imread('melisandre_cropped.jpg')
# edges = cv.Canny(duck,100,200)

# contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# outer_contour = np.zeros_like(edges)
# cv.drawContours(outer_contour, contours, 0, (255), 1)

# cv.imshow('result', edges)
# cv.waitKey(-1)
# cv.destroyAllWindows()

img = cv.imread('melisandre_cropped.jpg')
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
height, width = gray_img.shape

gray_img = 255 - gray_img
gray_img[gray_img > 100] = 255
gray_img[gray_img <= 100] = 0
black_padding = np.zeros((50, width))
gray_img = np.row_stack((black_padding, gray_img))

cv.imwrite('M1.jpg', gray_img)

kernel = np.ones((30, 30), np.uint8)
closing = cv.morphologyEx(gray_img, cv.MORPH_CLOSE, kernel)

cv.imwrite('M2.jpg', closing)

closing_copy = np.uint8(closing)
edges = cv.Canny(closing_copy, 100, 200)

cv.imwrite('melisandre_silhouette.jpg', edges)

# cv.imshow('result', edges)
# cv.waitKey(-1)
# cv.destroyAllWindows()