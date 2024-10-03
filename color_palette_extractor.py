import cv2
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def increase_saturation(image, scale=1.1):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv[..., 1] = cv2.multiply(hsv[..., 1], scale)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

def adjust_contrast(image, alpha=1.1, beta=5):
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return new_image

def weighted_pixel_sampling(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    brightness = hsv[..., 2]
    weights = brightness.flatten() / 255.0
    pixels = image.reshape(-1, 3)
    sampled_pixels = np.random.choice(np.arange(len(pixels)), size=len(pixels), p=weights/weights.sum())
    return pixels[sampled_pixels]

def extract_colors_gmm(image_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = increase_saturation(img, scale=saturation_scale)
    img = adjust_contrast(img, alpha=contrast_alpha, beta=contrast_beta)
    pixels = weighted_pixel_sampling(img)
    gmm = GaussianMixture(n_components=n_colors)
    gmm.fit(pixels)
    colors = gmm.means_.astype(int)

    hex_colors = [rgb_to_hex(color) for color in colors]
    print("Hex codes of top colors:", hex_colors)

    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    for i, color in enumerate(colors):
        ax[i].imshow([[color / 255]])
        ax[i].axis('off')
    plt.show()

image_path = r"pinterest_images\image_20240923_151746_587963.jpg"
n_colors = 5
extract_colors_gmm(image_path, n_colors, saturation_scale=1.1, contrast_alpha=1.1, contrast_beta=5)
