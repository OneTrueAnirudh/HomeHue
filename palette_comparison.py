from skimage import color
import numpy as np

def rgb2lab(pal):
    return color.rgb2lab(np.array(pal).reshape(-1, 1, 3) / 255).reshape(-1, 3)

def delta_e(lab1, lab2):
    return np.linalg.norm(lab1 - lab2)

def match_palette(target_pal_lab, dataset_pal_lab):
    total_dist = 0
    for target_color in target_pal_lab:
        closest_dist = min(delta_e(target_color, dataset_color) 
                               for dataset_color in dataset_pal_lab)
        total_dist += closest_dist
    return total_dist

def closest_palette(target_pal, dataset_pal):
    target_pal_lab = rgb2lab(target_pal)    
    best = None
    min_dist = float('inf')    
    for pal in dataset_pal:
        dataset_pal_lab = rgb2lab(pal)
        dist = match_palette(target_pal_lab, dataset_pal_lab)        
        if dist < min_dist:
            min_dist = dist
            best = pal
    
    return best, min_dist