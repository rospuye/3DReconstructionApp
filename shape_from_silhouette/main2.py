import cv2 as cv
import numpy as np
import open3d as o3d
from math import radians, sin, cos, inf
from os import path
import json
from color_segmenter import apply_mask
import itertools

num_pics = 15
angle = int(360/num_pics) # rotation in degrees between each perspective

rot_inc = radians(angle)
rot = 0
adjust = radians(90)

point_array = np.array([])

fileAlreadyExists = path.exists('limits.json')
if fileAlreadyExists:
    with open('limits.json', 'r') as openfile:
        json_object = json.load(openfile)
        ranges = json_object['limits']

# 
for i in range(1, num_pics+1):
    img = cv.imread('melisandre/screenshot (' + str(i) + ').jpg')

    # apply color filtering
    mask = apply_mask(img, ranges)
    color_filtered = cv.bitwise_and(img,img,mask = mask)
    color_filtered[np.where((color_filtered==[0,0,0]).all(axis=2))] = [255,255,255]

    # crop image
    h,w,_ = color_filtered.shape
    cropped_image = color_filtered[0:h-200, 0:w]

    # get silhouette
    gray_img = cv.cvtColor(cropped_image, cv.COLOR_BGR2GRAY)
    height, width = gray_img.shape
    gray_img = 255 - gray_img

    gray_img[gray_img > 100] = 255
    gray_img[gray_img <= 100] = 0
    black_padding = np.zeros((50, width))
    gray_img = np.row_stack((black_padding, gray_img))

    kernel = np.ones((30, 30), np.uint8)
    closing = cv.morphologyEx(gray_img, cv.MORPH_CLOSE, kernel)

    closing_copy = np.uint8(closing)
    edges = cv.Canny(closing_copy, 100, 200)

    # get point cloud from silhouette
    contour_idxs = np.where(edges == [255])
    Zs = [0] * np.shape(contour_idxs)[1]
    contour_coordinates = zip(contour_idxs[0], Zs, contour_idxs[1])
    contour_coordinates = list(contour_coordinates)
    contour_coordinates = np.array(contour_coordinates)
    contour_coordinates = contour_coordinates.reshape(-1, 3)

    pcl = o3d.geometry.PointCloud()
    pcl.points = o3d.utility.Vector3dVector(contour_coordinates)

    # translate to origin (for convenience)
    trans_m = np.array([0,0,0])
    pcl.translate(trans_m, relative=False)

    # rotate 90º around y
    rot_m = np.array([[cos(adjust), 0, sin(adjust)], [0, 1, 0], [-sin(adjust), 0, cos(adjust)]])
    pcl.rotate(rot_m)

    # do the rotations around z for the different perspectives
    rot_m = np.array([[cos(rot), -sin(rot), 0], [sin(rot), cos(rot), 0], [0, 0, 1]])
    pcl.rotate(rot_m)

    # bounding box to remove some outliers
    bounds = [[-500, 500], [-500, 500], [-100, 1600]]
    bounding_box_points = list(itertools.product(*bounds))
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points))

    pcl = pcl.crop(bounding_box)

    pcl_point_array = np.asarray(pcl.points)
    point_array = np.concatenate((point_array, pcl_point_array), axis=0) if point_array.any() else pcl_point_array

    rot += rot_inc

total_pcl = o3d.geometry.PointCloud()
total_pcl.points = o3d.utility.Vector3dVector(point_array)

uni_down_pcd = total_pcl.uniform_down_sample(every_k_points=20)
uni_down_pcd, _ = uni_down_pcd.remove_radius_outlier(nb_points=10, radius=120)

uni_down_pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=1, max_nn=30))

with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(uni_down_pcd, depth=12)
o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)


# Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(100)
# o3d.visualization.draw_geometries([uni_down_pcd])