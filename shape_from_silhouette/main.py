import cv2 as cv
import numpy as np
import open3d as o3d
from math import radians, sin, cos

angle = 5 # rotation in degrees between each perspective
num_pics = int(360/angle)

rot_inc = radians(angle)
rot = 0
adjust = radians(90)

point_array = np.array([])

for dir in ['y']:
    for i in range(1, num_pics):

        duck = cv.imread('strawberry/' + str(angle) + '/' + dir + '_turn/screenshot (' + str(i) + ').png')
        # duck = cv.imread('screenshots/screenshot (' + str(i) + ').png')
        edges = cv.Canny(duck,100,200)

        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        outer_contour = np.zeros_like(edges)
        cv.drawContours(outer_contour, contours, 0, (255), 1)

        contour_idxs = np.where(outer_contour == [255])
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

        if dir=='y':
            # rotate 90º around y
            rot_m = np.array([[cos(adjust), 0, sin(adjust)], [0, 1, 0], [-sin(adjust), 0, cos(adjust)]])
            pcl.rotate(rot_m)

            # do the rotations around z for the different perspectives
            rot_m = np.array([[cos(rot), -sin(rot), 0], [sin(rot), cos(rot), 0], [0, 0, 1]])
            pcl.rotate(rot_m)
        else:
            # rotate 90º around z
            rot_m = np.array([[cos(adjust), -sin(adjust), 0], [sin(adjust), cos(adjust), 0], [0, 0, 1]])
            pcl.rotate(rot_m)

            # rotate 90º around x
            rot_m = np.array([[1, 0, 0], [0, cos(-adjust), -sin(-adjust)], [0, sin(-adjust), cos(-adjust)]])
            pcl.rotate(rot_m)

            # do the rotations around z for the different perspectives
            rot_m = np.array([[cos(rot), 0, sin(rot)], [0, 1, 0], [-sin(rot), 0, cos(rot)]])
            pcl.rotate(rot_m)
            

        # o3d.visualization.draw_geometries([pcl])

        pcl_point_array = np.asarray(pcl.points)
        point_array = np.concatenate((point_array, pcl_point_array), axis=0) if point_array.any() else pcl_point_array

        rot += rot_inc

total_pcl = o3d.geometry.PointCloud()
total_pcl.points = o3d.utility.Vector3dVector(point_array)

center = np.array([0, 0, 0])
radius = 50

points = np.asarray(total_pcl.points)
distances = np.linalg.norm(points - center, axis=1)
total_pcl.points = o3d.utility.Vector3dVector(points[distances > radius])

uni_down_pcd = total_pcl.uniform_down_sample(every_k_points=20)

# uni_down_pcd.estimate_normals(
#     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=1, max_nn=30))

# with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
#     mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(uni_down_pcd, depth=12)
# o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)


# Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(100)
o3d.visualization.draw_geometries([uni_down_pcd])



# radii = [0.005, 0.01, 0.02, 0.04]
# rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
#     uni_down_pcd, o3d.utility.DoubleVector(radii))
# o3d.visualization.draw_geometries([uni_down_pcd, rec_mesh])


# alpha = 0.03
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(total_pcl, alpha)
# mesh.compute_vertex_normals()
# o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)







# edges_title = 'edges'
# w = int(1920/2)
# h = int(1080/2)
# cv.namedWindow(edges_title, cv.WINDOW_NORMAL)
# cv.resizeWindow(edges_title, w, h)

# cv.imshow(edges_title, outer_contour)
# cv.waitKey(-1)



    




