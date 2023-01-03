import cv2 as cv
import glob

# screenshots = glob.glob('strawberry//5//x_turn//screenshot (*).png')

# for fname in screenshots:
#     img = cv.imread(fname)
#     h,w,_ = img.shape
#     cropped_image = img[140:h-50, 0:int(w/2)]
#     # cropped_image = img[0:h, 0:(w-20)]
#     cv.imwrite(fname, cropped_image)

img = cv.imread('melisandre_result.jpg')
h,w,_ = img.shape
cropped_image = img[0:h-200, 0:w]
cv.imwrite('melisandre_cropped.jpg', cropped_image)
