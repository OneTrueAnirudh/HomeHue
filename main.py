#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings
import os
from palette_comparison import closest_palettes, wall_color_suggestions

#importing utility functions
from GUI import browse
from room_palette import extract_room_colors
from wall_segmenter import walls_user
from wall_color import extract_wall_color

#allowing user to select their picture
img_path=browse()

#segmenting wall regions from rest of the room
warnings.filterwarnings("ignore", category=FutureWarning)
img_mask,seg_img,mask=walls_user(img_path)

#extracting room colors from segmented image
n_colors = 4
room_colors=extract_room_colors(seg_img, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5)

#extracting wall color from the image mask
dominant_wall_color = extract_wall_color(img_mask)

#finding 3 closest palettes in the dataset to user's room
suggested_palettes=closest_palettes(room_colors,3)

#finding wall colors of closest palette rooms
wall_colors=wall_color_suggestions(suggested_palettes)
print(wall_colors)