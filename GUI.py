import tkinter as tk
from tkinter import filedialog
import cv2
import matplotlib.pyplot as plt

# Function to open a file browser and select an image
def open_file_browser():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    return file_path

# Function to read the selected image and display it using matplotlib
def read_and_display_image(image_path):
    img = cv2.imread(image_path)  # Read the image from the file path
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for proper display in matplotlib
    plt.imshow(img_rgb)  # Display the image using matplotlib
    plt.axis('off')  # Hide the axes
    plt.show()  # Show the image in the output

# Main function to browse, read, and display the image
def browse():
    image_path = open_file_browser()  # Open the file browser and get the selected file path
    if image_path:
        read_and_display_image(image_path)  # Display the image using the selected file path

    return image_path  # Return the path to the image for further use

# img=browse()
# print(img)