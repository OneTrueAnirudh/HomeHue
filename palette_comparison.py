from skimage import color
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

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

def visualize_top_palette(palette, i):
    palette = np.array(palette) / 255  # Normalize RGB values to 0-1 range
    fig, ax = plt.subplots(1, len(palette), figsize=(len(palette) * 2, 2))
    
    for j, color in enumerate(palette):
        ax[j].imshow([[color]])  # Display each color as a square
        ax[j].axis('off')  # Hide axes for clean display
    
    # Set the title as "Top i Palette"
    fig.suptitle(f"Top {i+1} Palette", fontsize=16, fontweight='bold')
    plt.show()


def get_room_colors_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    if 'room_colors' in df.columns:
        room_colors_list = df['room_colors'].tolist()
        return room_colors_list
    else:
        print("'room_colors' column not found in the CSV file.")
        return []

def closest_palettes(target_pal, top_n=3):
    dataset_pal = get_room_colors_from_csv('dataset.csv')
    target_pal_lab = rgb2lab(target_pal)
    closest_palettes = [] 
    for pal_str in dataset_pal:
        try:
            pal = ast.literal_eval(pal_str)
        except ValueError:
            print(f"Error converting palette: {pal_str}")
            continue
        if isinstance(pal, list):
            pal = tuple(tuple(color) for color in pal)
        if isinstance(pal, tuple) and all(isinstance(c, tuple) and len(c) == 3 for c in pal):
            dataset_pal_lab = rgb2lab(pal)
            dist = match_palette(target_pal_lab, dataset_pal_lab)
            closest_palettes.append((pal, dist))
            # Sort the list and retain only the top N closest palettes
            closest_palettes = sorted(closest_palettes, key=lambda x: x[1])[:top_n]
        else:
            print(f"Invalid palette format: {pal_str}")
    for i, (palette, distance) in enumerate(closest_palettes):
        print(f"Top {i+1} Palette (Distance: {distance})")
        visualize_top_palette(palette,i)
    return closest_palettes
