import cv2 as cv
import numpy as np
import open3d as o3d
from math import radians, sin, cos

duck = cv.imread('images/duck_on_white/duck4.png')
edges = cv.Canny(duck,100,200)

contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
outer_contour = np.zeros_like(edges)
cv.drawContours(outer_contour, contours, 0, (255), 1)

edges_title = 'edges'
w = int(1920/2)
h = int(1080/2)
cv.namedWindow(edges_title, cv.WINDOW_NORMAL)
cv.resizeWindow(edges_title, w, h)

cv.imshow(edges_title, outer_contour)
cv.waitKey(-1)
cv.destroyAllWindows()