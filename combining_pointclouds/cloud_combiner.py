import numpy as np
import open3d as o3d
import glob
from copy import copy
from math import pi, sin, cos, radians, inf
import itertools

clouds = glob.glob('clouds//joker//*.ply')

final_cloud = o3d.io.read_point_cloud(clouds[0])
rot_inc = radians(20)
rot = rot_inc


meshes = []
i = 1
for pc_f in clouds[1:]:

    pc = o3d.io.read_point_cloud(pc_f)

    # translate to origin
    trans_m = np.array([0,0,0])
    pc.translate(trans_m, relative=False)

    # bounding box to remove wall points
    bounds = [[-0.1, 0.05], [-0.1, 0.05], [-inf, inf]]
    bounding_box_points = list(itertools.product(*bounds))
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points))
    pc = pc.crop(bounding_box)

    # clean out noise (remove statistical outliers)
    voxel_down_pc = pc.voxel_down_sample(voxel_size=0.02)
    pc, ind = voxel_down_pc.remove_statistical_outlier(nb_neighbors=50, std_ratio=10)

    # # apply rotations
    # rot_m = np.array([[cos(rot), -sin(rot), 0], [sin(rot), cos(rot), 0], [0, 0, 1]])
    # pc.rotate(rot_m)

    meshes.append(copy(pc))

    final_cloud.points = o3d.utility.Vector3dVector(np.vstack((np.asarray(final_cloud.points), np.asarray(pc.points))))
    final_cloud.colors = o3d.utility.Vector3dVector(np.vstack((np.asarray(final_cloud.colors), np.asarray(pc.colors))))

    rot += rot_inc
    i += 1

# Create axes mesh
Axes = o3d.geometry.TriangleMesh.create_coordinate_frame(0.5)
meshes.append(Axes)

o3d.visualization.draw_geometries(meshes)