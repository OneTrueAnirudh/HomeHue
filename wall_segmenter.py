from models.models import SegmentationModule, build_encoder, build_decoder
from src.eval import segment_image
from utils.constants import DEVICE
from utils.utils import images
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def display_output(original_image, masked_image, segmented_image):

    # Display original image
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for matplotlib
    plt.title('Original Image')
    plt.axis('off')

    # Display masked image
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for matplotlib
    plt.title('Masked Image')
    plt.axis('off')

    # Display segmented image
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for matplotlib
    plt.title('Segmented Image')
    plt.axis('off')

    plt.show()

def segment_walls(path_image, weights_encoder, weights_decoder):
    print("segmenting walls from image...")
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
    print("segmenting walls from image...")
    script_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(script_path)
    weights_encoder = os.path.join(base_dir, "model_weights", "encoder_weight.pth")
    weights_decoder = os.path.join(base_dir, "model_weights", "decoder_weight.pth")
    mask = segment_walls(path_image, weights_encoder, weights_decoder)
    orig = cv2.imread(path_image)
    m, s = images(orig, mask)
    m = np.asarray(m)
    s = np.asarray(s)
    cv2.imwrite(os.path.join(base_dir, "user_room_img.jpg"), s)
    display_output(orig,m,s)   
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
    display_output(orig,m,s)
    return m,s

# if __name__=="__main__":
#     img_path=r"pinterest_images\image_20241003_002805_245924.jpg"
#     walls_ui(img_path)
