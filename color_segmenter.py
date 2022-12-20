import cv2
from functools import partial
import json
from os import path

def update_range_dict(val,ranges,color,bound):
    ranges[color][bound] = val

def apply_mask(image, ranges):
    lows = (ranges['B']['min'], ranges['G']['min'], ranges['R']['min'])
    highs = (ranges['B']['max'], ranges['G']['max'], ranges['R']['max'])
    return cv2.inRange(image, lows, highs)

def main():

    # # get the color range values to start with
    # # if we already have a 'limits.json' file in the directory, we get the previously saved values from there
    # fileAlreadyExists = path.exists('limits.json')
    # if fileAlreadyExists:
    #     with open('limits.json', 'r') as openfile:
    #         json_object = json.load(openfile)
    #         ranges = json_object['limits']
    # # if not, we start with default values
    # else:
    ranges = { 'B':{'max': 255, 'min': 0}, 'G':{'max': 255, 'min': 0}, 'R':{'max': 255, 'min': 0} }

    img = cv2.imread('images/melisandre/melisandre0.jpg')

    # figure out window size from the size of the image
    scale = 0.55
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0])

    # finish up the video capture setup
    window_name = 'Color segmentation'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)

    # max value for all the trackbars
    slider_max = 255

    # trackbars for R, G and B dimensions

    cv2.createTrackbar('R min', window_name , ranges['R']['min'], slider_max, partial(update_range_dict, ranges=ranges, color='R', bound='min'))
    cv2.createTrackbar('R max', window_name , ranges['R']['max'], slider_max, partial(update_range_dict, ranges=ranges, color='R', bound='max'))
    
    cv2.createTrackbar('G min', window_name , ranges['G']['min'], slider_max, partial(update_range_dict, ranges=ranges, color='G', bound='min'))
    cv2.createTrackbar('G max', window_name , ranges['G']['max'], slider_max, partial(update_range_dict, ranges=ranges, color='G', bound='max'))
    
    cv2.createTrackbar('B min', window_name , ranges['B']['min'], slider_max, partial(update_range_dict, ranges=ranges, color='B', bound='min'))
    cv2.createTrackbar('B max', window_name , ranges['B']['max'], slider_max, partial(update_range_dict, ranges=ranges, color='B', bound='max'))

    # color segmentation continuous operation
    while True:

        # apply color segmentation mask to the recently captured frame 
        mask = apply_mask(img, ranges)
        cv2.imshow(window_name, mask)

        # wait for a command
        pressedKey = cv2.waitKey(1) & 0xFF

        # Quit
        if pressedKey == ord('q'):
            break
        # Write to file
        elif pressedKey == ord('w'):
            data = {'limits' : ranges}
            json_object = json.dumps(data, indent=4)
            with open("limits.json", "w") as outfile:
                outfile.write(json_object)
            break



if __name__ == '__main__':
    main()