
import numpy as np
import cv2
import glob

board_h = 9
board_w = 6

def  FindAndDisplayChessboard(img):
    # Find the chess board corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (board_w,board_h),None) # VERY SLOW IMAGE PAIRS: 4, 10

    # If found, display image with corners
    if ret == True:
        img = cv2.drawChessboardCorners(img, (board_w, board_h), corners, ret)
        cv2.namedWindow('calibration', cv2.WINDOW_NORMAL)
        cv2.imshow('calibration',img)
        cv2.waitKey(500)

    return ret, corners

objp = np.zeros((board_w*board_h,3), np.float32)
objp[:,:2] = np.mgrid[0:board_w,0:board_h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
left_points = [] # 2d points in image plane.
right_points = []

# Read images
images_left = glob.glob('images//calibration//left//left*.jpg')
images_right = glob.glob('images//calibration//right//right*.jpg')

mtxL, distL = None, None
for fname in images_left:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = FindAndDisplayChessboard(img)
    if ret == True:
        objpoints.append(objp)
        left_points.append(corners)


mtxR, distR = None, None
for fname in images_right:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = FindAndDisplayChessboard(img)
    if ret == True:
        right_points.append(corners)

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints, left_points, right_points, None, None, None, None, (board_h, board_w), flags=cv2.CALIB_SAME_FOCAL_LENGTH)

cv2.destroyAllWindows()

np.savez("stereoParams.npz",
    intrinsics1=cameraMatrix1,
    distortion1=distCoeffs1,
    intrinsics2=cameraMatrix2,
    distortion2=distCoeffs2,
    R=R, T=T, E=E, F=F)