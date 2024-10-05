import matplotlib.pyplot as plt
from models.models import SegmentationModule, build_encoder, build_decoder
from src.eval import segment_image
from utils.constants import DEVICE
from utils.utils import images
import cv2
import numpy as np
import os

def segment_walls(path_image, weights_encoder, weights_decoder):
    """
    Function to perform wall segmentation on a given image.
    
    Parameters:
    - path_image: Path to the input image.
    - weights_encoder: Path to the encoder model weights.
    - weights_decoder: Path to the decoder model weights.
    
    Returns:
    - segmentation_mask: The segmentation mask of the input image.
    """
    # Build the encoder and decoder models
    net_encoder = build_encoder(weights_encoder)
    net_decoder = build_decoder(weights_decoder)

    # Initialize the segmentation module
    segmentation_module = SegmentationModule(net_encoder, net_decoder)
    segmentation_module = segmentation_module.to(DEVICE).eval()

    # Predict the segmentation mask for the input image
    segmentation_mask = segment_image(segmentation_module, path_image)

    # Return the segmentation mask
    return segmentation_mask

def walls_ui(path_image): #same function but it just saves the segmented image without the walls
    script_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(script_path)
    weights_encoder = os.path.join(base_dir, "model_weights", "encoder_weight.pth")
    weights_decoder = os.path.join(base_dir, "model_weights", "decoder_weight.pth")
    mask = segment_walls(path_image, weights_encoder, weights_decoder)
    orig = cv2.imread(path_image)
    m, s = images(orig, mask)
    m = np.asarray(m)
    s = np.asarray(s)
    cv2.imwrite(os.path.join(base_dir, "seg.jpg"), s)   
    return m

def walls(path_image):    
    script_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(script_path)
    weights_encoder = os.path.join(base_dir, "model_weights", "encoder_weight.pth")
    weights_decoder = os.path.join(base_dir, "model_weights", "decoder_weight.pth")
    mask = segment_walls(path_image, weights_encoder, weights_decoder)
    orig = cv2.imread(path_image)
    m, s = images(orig, mask)
    m = np.asarray(m)
    s = np.asarray(s)
    return m,s  

if __name__=="__main__":
    script_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(script_path)
    img = os.path.join(base_dir, "pinterest_images", "image_20240923_151750_809916.jpg")
    walls(img)
