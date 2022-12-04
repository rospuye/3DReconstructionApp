import numpy as np
import open3d as o3d
import argparse
import os

# parse command line arguments
parser = argparse.ArgumentParser(description='3D Reconstruction of small objects')
parser.add_argument('-o', '--object', type=str, required=True, help='Indicate which object you want to view.')
args = vars(parser.parse_args())
object = args["object"]

# check if we have the necessary data on the specified object
image_path = 'images/' + object
data3d_path = '3d_data/' + object
if not os.path.exists(image_path) or not os.path.exists(data3d_path):
    print("Oh no! There isn't enough data on this object for a visualization!")
    exit()

# load 3D reprojections
DIR = 'images/' + object
num_imgs = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

points_3D = np.empty(0)
for perspective in range(num_imgs):
    with np.load('3d_data/' + object + '/3DParams' + str(perspective) + '.npz') as data:
        points_3D = np.concatenate((points_3D, data['proj3D']))

# reshape and filter the points
# TODO: filter them properly
p = points_3D.reshape(-1, 3)
fp = []
for i in range(p.shape[0]):
    if np.all(~np.isinf(p[i])):
        # if p[i][2]<16:
        fp.append(p[i])


# visualize the pointcloud
pcl = o3d.geometry.PointCloud()
pcl.points = o3d.utility.Vector3dVector(fp)

Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(1) # create axes mesh
o3d.visualization.draw_geometries([pcl , Axes]) # show meshes in view

