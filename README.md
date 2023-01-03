# 3DReconstructionApp
An OpenCV application for 3D reconstruction of small objects. This project was developed for the Computer Vision course at University of Aveiro, 2022/2023.

### Students

| Name   | Student ID  |
|---|---|
| Diogo Monteiro   | 97606  |
| Isabel Rosário  | 93343   |

Given the exploratory nature of this project, this repository is a bit of an amalgam of everything we tried to do: the successful attempts and everything else as well. That being said, we found it important to write a sort of small manual just to explain what is what.

## Important Files

### `combining_point_clouds`

This folder contains code for the purpose of taking several PointClouds of the same object and trying to clean their noise and combine them. We used this to combine several PointClouds obtained with Tango.

### `shape_from_silhouette`

This contains all the code concerning the "shape from silhouette" reconstruction attempt, which was the most successful one we tried. Besides lots of test images, it contains several files for different purposes:
- `color_segmenter` performs color segmentation to help remove the background from the several point of view pictures;
- `crop_images` crops images in batch;
- `filter_object` filters out the pixels pertaining to the object of interest;
- `get_silhouette` uses the output from `filter_object` to compute the object's silhouette;
- `main2` performs the main operations of computing the PointClouds from the silhouettes, as well as cleaning some of their noise and combining them;
- `main` was an older version of `main2` used for the same purpose, but for the images obtained with the small Web app we developed (explained below), which didn't require as many steps as the "real" pictures.

### `frontend`

This folder contains a small Web app we developed for the sake of testing the silhouette method with virtual objects. This was a good testing opportunity because the environment was completely controllable and we didn't have to deal with problems such as camera distortion. This Web app is contained in a Webpack package - if you wish to run it, run `npm install` inside the `frontend` folder, followed by `npm run dev`.

### `sift`

This folder contains all the code pertaining to our attempt to use SIFT to find points of special interest in the object, match them across different points of view of the object and build a 3D model from there. This attempt was not successful.

### Other

All the Python scripts on the home directory are related to our initial attempt to perform "structure from motion", which was not successful. We used concepts from class to take picture around the object and treat each pair of consecutive images as a stereo pair.
