import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def display_dominant_color(color):
    # Create an image (box) filled with the dominant color
    color_box = np.zeros((100, 100, 3), dtype=np.uint8)
    color_box[:] = color
    
    # Convert the color box to the range [0, 1] for matplotlib
    color_box = color_box / 255.0
    
    # Display the color box using matplotlib
    plt.imshow(color_box)
    plt.axis('off')  # Turn off the axis
    plt.title("Wall Color")
    plt.show()

def extract_wall_color(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the HSV range for bright green (greenscreen) color
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    
    # Create a mask for the green pixels
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    
    # Invert the mask to focus on the wall regions
    wall_mask = cv2.bitwise_not(green_mask)
    
    # Apply the wall mask to the original image
    wall_regions = cv2.bitwise_and(image, image, mask=wall_mask)
    
    # Reshape the wall region image to a list of pixels
    pixels = wall_regions.reshape(-1, 3)
    
    # Remove the black (background) pixels
    pixels = np.array([pixel for pixel in pixels if not np.all(pixel == 0)])
    
    # If no pixels remain, return None
    if len(pixels) == 0:
        return None
    
    # Apply K-means clustering to find the dominant color
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(pixels)
    
    # Get the cluster center (the dominant color) and convert to RGB
    dominant_color_bgr = kmeans.cluster_centers_[0].astype(int)
    dominant_color_rgb = dominant_color_bgr[::-1]  # Convert BGR to RGB

    print("wall color (RGB): ", dominant_color_rgb)

    display_dominant_color(dominant_color_rgb)

    return tuple(dominant_color_rgb)
