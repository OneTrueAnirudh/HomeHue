import cv2
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

# Helper function to convert RGB to Hex format
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

# Function to increase saturation of an image
def increase_saturation(image, scale=1.1):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # Convert image to HSV color space
    hsv[..., 1] = cv2.multiply(hsv[..., 1], scale)  # Multiply saturation channel by the scale
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)  # Convert back to RGB

# Function to adjust contrast and brightness of an image
def adjust_contrast(image, alpha=1.1, beta=5):
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)  # Apply contrast and brightness adjustments
    return new_image

# Function to perform weighted sampling of pixels based on brightness
def weighted_pixel_sampling(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # Convert image to HSV color space
    brightness = hsv[..., 2]  # Extract brightness (value) channel
    weights = brightness.flatten() / 255.0  # Normalize brightness values to use as weights
    pixels = image.reshape(-1, 3)  # Flatten the image into a list of RGB pixel values
    sampled_pixels = np.random.choice(np.arange(len(pixels)), size=len(pixels), p=weights / weights.sum())  # Sample pixels based on brightness weights
    return pixels[sampled_pixels]

# Function to apply GMM for color extraction from an image
def extract_colors_gmm(image_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5):
    img = cv2.imread(image_path)  # Read the image from the specified path
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the image from BGR (OpenCV) to RGB
    img = increase_saturation(img, scale=saturation_scale)  # Increase the saturation of the image
    img = adjust_contrast(img, alpha=contrast_alpha, beta=contrast_beta)  # Adjust contrast and brightness of the image
    pixels = weighted_pixel_sampling(img)  # Perform weighted sampling of pixels

    # Fit a Gaussian Mixture Model to identify n_colors dominant colors
    gmm = GaussianMixture(n_components=n_colors)
    gmm.fit(pixels)
    colors = gmm.means_.astype(int)  # Extract the mean RGB values of the clusters

    # Convert the RGB colors to Hex format and print them
    hex_colors = [rgb_to_hex(color) for color in colors]
    print("Hex codes of top colors:", hex_colors)

    # Display the color palette as consecutive squares
    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    for i, color in enumerate(colors):
        ax[i].imshow([[color / 255]])  # Show each color as a square
        ax[i].axis('off')  # Hide axis for a cleaner display
    plt.show()

# Function to remove green pixels (greenscreen areas) from the image
def remove_green_pixels(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # Convert image to HSV color space
    # Define the range for green color in HSV
    lower_green = np.array([40, 40, 40])  # Lower bound of green in HSV
    upper_green = np.array([80, 255, 255])  # Upper bound of green in HSV
    
    # Create a mask to filter out green pixels
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert the mask to keep only non-green pixels
    non_green_image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    
    return non_green_image

# Modified function to apply GMM for color extraction excluding green pixels
def extract_colors_gmm_no_green(image_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5):
    img = cv2.imread(image_path)  # Read the image from the specified path
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the image from BGR (OpenCV) to RGB
    img = remove_green_pixels(img)  # Remove green pixels from the image
    img = increase_saturation(img, scale=saturation_scale)  # Increase the saturation of the image
    img = adjust_contrast(img, alpha=contrast_alpha, beta=contrast_beta)  # Adjust contrast and brightness of the image
    pixels = weighted_pixel_sampling(img)  # Perform weighted sampling of pixels

    # Fit a Gaussian Mixture Model to identify n_colors dominant colors
    gmm = GaussianMixture(n_components=n_colors)
    gmm.fit(pixels)
    colors = gmm.means_.astype(int)  # Extract the mean RGB values of the clusters

    # Convert the RGB colors to Hex format and print them
    hex_colors = [rgb_to_hex(color) for color in colors]
    print("Hex codes of top colors:", hex_colors)

    # Display the color palette as consecutive squares
    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    for i, color in enumerate(colors):
        ax[i].imshow([[color / 255]])  # Show each color as a square
        ax[i].axis('off')  # Hide axis for a cleaner display
    plt.show()

# image_path = r""
# extract_colors_gmm_no_green(image_path, n_colors=5)
