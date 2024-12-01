import cv2
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

# # Helper function to convert RGB to Hex format
# def rgb_to_hex(rgb):
#     return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

# Function to increase saturation of an image
def increase_saturation(image, scale=1.1):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  
    hsv[..., 1] = cv2.multiply(hsv[..., 1], scale)  
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)  

# Function to adjust contrast and brightness of an image
def adjust_contrast(image, alpha=1.1, beta=5):
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)  
    return new_image

# Function to perform weighted sampling of pixels based on brightness
def weighted_pixel_sampling(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  
    brightness = hsv[..., 2]  
    weights = brightness.flatten() / 255.0  
    pixels = image.reshape(-1, 3)  
    sampled_pixels = np.random.choice(np.arange(len(pixels)), size=len(pixels), p=weights / weights.sum())  # Sample pixels based on brightness weights
    return pixels[sampled_pixels]

# Function to remove green pixels (greenscreen areas) from the image
def remove_green_pixels(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) 

    # Define the range for green color in HSV
    lower_green = np.array([40, 40, 40]) 
    upper_green = np.array([80, 255, 255]) 

    mask = cv2.inRange(hsv, lower_green, upper_green)
    non_green_image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))    
    return non_green_image

# Modified function to apply GMM for color extraction excluding green pixels
def extract_room_colors(img, n_colors=4, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5):
    print("extracting room's color palette...")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    img = remove_green_pixels(img)  
    img = increase_saturation(img, scale=saturation_scale)  
    img = adjust_contrast(img, alpha=contrast_alpha, beta=contrast_beta)  
    pixels = weighted_pixel_sampling(img)  
    gmm = GaussianMixture(n_components=n_colors)
    gmm.fit(pixels)
    colors = gmm.means_.astype(int)  
    print("RGB values of dominant colors:\n", colors)
    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    for i, color in enumerate(colors):
        ax[i].imshow([[color / 255]])  
        ax[i].axis('off') 
    fig.suptitle("Room Color Palette", x=0.5, fontsize=16, fontweight='bold')
    plt.show()

    return list(map(tuple, colors))

# image_path = r""  # Replace with your image path
# room_colors = extract_room_colors(image_path, n_colors=4)
# print("Extracted Room Colors (RGB):", room_colors)
