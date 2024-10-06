import numpy as np
import cv2
from utils.utils import hex_to_rgb

def post_proc(image, mask, target_color, alpha=0.5):
    target_color = list(hex_to_rgb(target_color))
    color_image = np.zeros_like(image)
    color_image[:] = target_color  
    mask = (mask == 0).astype(np.uint8) * 255
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)  
    color_overlay = cv2.bitwise_and(color_image, color_image, mask=mask)
    blended_image = cv2.addWeighted(gray_image, 1 - alpha, color_overlay, alpha, 0)
    result_image = np.where(mask[..., None] == 255, blended_image, image)
    return result_image