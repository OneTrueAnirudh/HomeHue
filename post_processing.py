import numpy as np
import cv2
from utils.utils import hex_to_rgb
import matplotlib.pyplot as plt

def post_process(image, mask, target_color, alpha=0.5):
    target_color = list(hex_to_rgb(target_color))
    target_color = target_color[::-1]
    color_image = np.zeros_like(image)
    color_image[:] = target_color  
    mask = (mask == 0).astype(np.uint8) * 255
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)  
    color_overlay = cv2.bitwise_and(color_image, color_image, mask=mask)
    blended_image = cv2.addWeighted(gray_image, 1 - alpha, color_overlay, alpha, 0)
    result_image = np.where(mask[..., None] == 255, blended_image, image)
    return result_image

def apply_wall_colors(image_path, mask, wall_colors, alpha=0.5): #doesnt work rn
    processed_images = []

    image=cv2.imread()

    # Process each suggested wall color and store the result
    for color in wall_colors:
        result_image = post_process(image, mask, color, alpha=alpha)
        processed_images.append(result_image)

    # Plot all processed images in subplots
    fig, axes = plt.subplots(1, len(wall_colors), figsize=(len(wall_colors) * 5, 5))

    for i, img in enumerate(processed_images):
        # Convert BGR (OpenCV format) to RGB for plotting
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the image in the corresponding subplot
        axes[i].imshow(img_rgb)
        axes[i].axis('off')  # Hide axes for a cleaner look
        axes[i].set_title(f'Room Idea {i+1}')

    # Set the overall title
    fig.suptitle("Room Aesthetic Suggestions", fontsize=16)

    # Adjust layout for better spacing
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()