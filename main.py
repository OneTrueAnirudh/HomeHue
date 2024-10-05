#importing libraries

import cv2

#importing utility functions

from GUI import browse
from color_palette_extractor import extract_colors_gmm

img_path=r'seg\seg_1.jpg'

#extracting colors from the dataset image

n_colors = 5
extract_colors_gmm(img_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5)