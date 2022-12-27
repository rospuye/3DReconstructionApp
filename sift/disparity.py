import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import open3d as o3d

imgL = cv.imread('melisandre/1.jpg',0)
# imgL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)

imgR = cv.imread('melisandre/2.jpg',0)
# imgR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)

# plt.imshow(disparity,'gray')
# plt.show()

h, w = imgL.shape[:2]
f = 0.8 * w  # guess for focal length
Q = np.float32([[1, 0, 0, -0.5 * w],
                [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
                [0, 0, 0, -f],  # so that y-axis looks up
                [0, 0, 1, 0]])

points3d = cv.reprojectImageTo3D(disparity, Q)

p = points3d.reshape(-1, 3)
fp = []
for i in range(p.shape[0]):
    if np.all(~np.isinf(p[i])):
        if p[i][2]<16:
            fp.append(p[i])


# visualize the pointcloud
pcl = o3d.geometry.PointCloud()
pcl.points = o3d.utility.Vector3dVector(fp)

Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(1) # create axes mesh
o3d.visualization.draw_geometries([pcl , Axes]) # show meshes in view