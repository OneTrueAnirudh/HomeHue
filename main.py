#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings
import os

#importing utility functions
from GUI import browse
from room_palette import extract_room_colors
from images import walls_ui
from wall_color import extract_wall_color

#allowing user to select their picture
img_path=browse()

#segmenting wall regions from rest of the room
warnings.filterwarnings("ignore", category=FutureWarning)
img_mask=walls_ui(img_path)

#extracting room colors from segmented image
seg_img_path=r'user_room_img.jpg'
n_colors = 4
color_palette=extract_room_colors(seg_img_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5)

#extracting wall color from the image mask
dominant_wall_color = extract_wall_color(img_mask)

#deleting the user_room file
if os.path.isfile(r'user_room_img.jpg'):
        os.remove(r'user_room_img.jpg')