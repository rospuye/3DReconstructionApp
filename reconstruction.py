import numpy as np
import cv2
import os
import argparse
from sys import exit

# parse command line arguments
parser = argparse.ArgumentParser(description='3D Reconstruction of small objects')
parser.add_argument('-o', '--object', type=str, required=False, help='Indicate which object you want to do a 3D reconstruction of.')
args = vars(parser.parse_args())
object = args["object"]

# load camera parameters
with np.load('stereoParams.npz') as data:
    intrinsics1 = data['intrinsics1']
    distortion1 = data['distortion1']
    intrinsics2 = data['intrinsics2']
    distortion2 = data['distortion2']
    R = data['R']
    T = data['T']
    E = data['E']
    F = data['F']

if not object:
    object = 'melisandre' # default object
else:
    if not os.path.exists('images/' + object):
        print("Oh no! There are no available pictures of this object!")
        exit()

DIR = 'images/' + object
num_imgs = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

# if folder for 3D data doesn't exist, create it
if not os.path.exists('3d_data'):
    os.mkdir('3d_data')
if not os.path.exists('3d_data/' + object):
    os.mkdir('3d_data/' + object)



# for each pair of images, compute the 3D data
for perspective in range(num_imgs):
    left_idx = perspective
    right_idx = (perspective + 1) % num_imgs # last image pairs with first image again for full circularity

    # reading images
    left = cv2.imread('images/' + object + '/' + object + str(left_idx) + '.jpg')
    undistort_left = cv2.undistort(left, intrinsics1, distortion1)

    right = cv2.imread('images/' + object + '/' + object + str(right_idx) + '.jpg')
    undistort_right = cv2.undistort(right, intrinsics2, distortion2)

    height, width, depth =  undistort_left.shape

    R1 = np.zeros(shape=(3,3))
    R2 = np.zeros(shape=(3,3))
    P1 = np.zeros(shape=(3,4))
    P2 = np.zeros(shape=(3,4))
    Q = np.zeros(shape=(4,4))

    cv2.stereoRectify(intrinsics1, distortion1, intrinsics2, distortion2 ,(width, height), R, T, R1, R2, P1, P2, Q, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(0,0))

    # map computation
    map1x, map1y = cv2.initUndistortRectifyMap(intrinsics1, distortion1, R1, P1, (width,height), cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(intrinsics2, distortion2, R2, P2, (width,height), cv2.CV_32FC1)

    # cv2.namedWindow('map', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('map', 300, 700)
    # cv2.imshow('map', map1x)

    # cv2.waitKey(-1)

    # image remapping
    remap_imgl = None
    gray_imagel = cv2.cvtColor(undistort_left, cv2.COLOR_BGR2GRAY)
    remap_imgl = cv2.remap(gray_imagel, map1x, map1y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

    remap_imgr = None
    gray_imager = cv2.cvtColor(undistort_right, cv2.COLOR_BGR2GRAY)
    remap_imgr = cv2.remap(gray_imager, map2x, map2y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

    # cv2.namedWindow('left', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('left', 300, 700)
    # cv2.imshow('left', remap_imgl)

    # cv2.namedWindow('right', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('right', 300, 700)
    # cv2.imshow('right', remap_imgr)

    # cv2.waitKey(-1)

    # call the constructor for StereoBM
    stereo = cv2.StereoBM_create(numDisparities=16*5, blockSize=21)

    # calculate the disparity image
    disparity = stereo.compute(remap_imgl,remap_imgr)

    disparity = cv2.normalize(src=disparity, dst=disparity, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
    disparity = np.uint8(disparity)

    reprojection3D = cv2.reprojectImageTo3D(disparity, Q)

    np.savez('3d_data/' + object + '/3DParams' + str(perspective) + '.npz', proj3D=reprojection3D)

