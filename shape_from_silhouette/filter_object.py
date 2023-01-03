import cv2
from os import path
import json
from color_segmenter import apply_mask
import numpy as np

fileAlreadyExists = path.exists('limits.json')
if fileAlreadyExists:
    with open('limits.json', 'r') as openfile:
        json_object = json.load(openfile)
        ranges = json_object['limits']

img = cv2.imread('melisandre.jpg')
mask = apply_mask(img, ranges)

res = cv2.bitwise_and(img,img,mask = mask)
res[np.where((res==[0,0,0]).all(axis=2))] = [255,255,255]

cv2.imwrite('melisandre_result.jpg', res)

# cv2.imshow('result', res)
# cv2.waitKey(-1)
# cv2.destroyAllWindows()