from skimage import color
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
import cv2

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
    palette = np.array(palette) / 255
    fig, ax = plt.subplots(1, len(palette), figsize=(len(palette) * 2, 2))
    for j, color in enumerate(palette):
        ax[j].imshow([[color]])
        ax[j].axis('off')
    fig.suptitle(f"Top {i+1} Palette", fontsize=16, fontweight='bold')
    plt.show()


def get_room_colors(csv_file):
    df = pd.read_csv(csv_file)
    if 'room_colors' in df.columns:
        room_colors_list = df['room_colors'].tolist()
        return room_colors_list
    else:
        print("'room_colors' column not found in the CSV file.")
        return []

def closest_palettes(target_pal, top_n=3):
    dataset_pal = get_room_colors('dataset.csv')
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
            closest_palettes = sorted(closest_palettes, key=lambda x: x[1])[:top_n]
        else:
            print(f"Invalid palette format: {pal_str}")
    for i, (palette, distance) in enumerate(closest_palettes):
        print(f"Top {i+1} Palette (Distance: {distance})")
        visualize_top_palette(palette,i)
    return closest_palettes

def find_wall_color(csv_file, target_palette):
    df = pd.read_csv(csv_file)
    for idx, row in df.iterrows():
        try:
            row_palette = ast.literal_eval(row['room_colors'])
            if isinstance(row_palette, list):
                row_palette = tuple(tuple(color) for color in row_palette)
            if row_palette == target_palette:
                return ast.literal_eval(row['wall_color'])
        except (ValueError, SyntaxError):
            print(f"Error parsing palette in row {idx}") 
    return None

def wall_color_suggestions(suggested_palettes):
    sp = [palette[0] for palette in suggested_palettes] 
    wall_colors = []
    fig, axes = plt.subplots(1, len(sp), figsize=(len(sp) * 2, 2))
    for i, palette in enumerate(sp):
        suggested_wall_color = find_wall_color('dataset.csv', palette)
        wall_colors.append(suggested_wall_color)
        color_square = np.array([[suggested_wall_color]]) / 255.0
        axes[i].imshow(color_square)
        axes[i].set_title('Wall Color ' + str(i+1))
        axes[i].axis('off') 
    fig.suptitle('Suggested Wall Colors', fontsize=16)
    plt.tight_layout()
    plt.show()
    return wall_colors

def find_room_idea(csv_file, target_palette):
    df = pd.read_csv(csv_file)
    for idx, row in df.iterrows():
        try:
            row_palette = ast.literal_eval(row['room_colors'])
            if isinstance(row_palette, list):
                row_palette = tuple(tuple(color) for color in row_palette)
            if row_palette == target_palette:
                return str(row['image_path'])
        except (ValueError, SyntaxError):
            print(f"Error parsing palette in row {idx}") 
    return None

def room_idea_suggestions(suggested_palettes):
    sp = [palette[0] for palette in suggested_palettes] 
    fig, axes = plt.subplots(1, len(sp), figsize=(len(sp) * 2, 2))
    for ind, i in enumerate(sp):
        suggested_room_idea = find_room_idea('dataset.csv', i)
        img = cv2.cvtColor(cv2.imread(suggested_room_idea), cv2.COLOR_BGR2RGB)
        img=img/255.0
        axes[ind].imshow(img)
        axes[ind].set_title('Room Idea' + str(ind+1))
        axes[ind].axis('off') 
    fig.suptitle('Suggested Room Ideas', fontsize=16)
    plt.tight_layout()
    plt.show()
