import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch
from PIL import Image

def hexagon(center, size):
    angles_hex = np.linspace(0, 2 * np.pi, 7)
    hexagon_points = [(center[0] + size * np.cos(a), center[1] + size * np.sin(a)) for a in angles_hex]
    top_apex = (center[0], center[1] + np.sqrt(3) * size)
    bottom_apex = (center[0], center[1] - np.sqrt(3) * size)
    top_triangle = [hexagon_points[1], top_apex, hexagon_points[2]]
    bottom_triangle = [hexagon_points[4], bottom_apex, hexagon_points[5]]
    return hexagon_points[:-1], top_triangle, bottom_triangle

def add_point(point, points, point_indices):
    if point not in point_indices:
        point_indices[point] = len(points)
        points.append(point)
    return point_indices[point]

def create_shape(points, point_indices, shape):
    shape_indices = []
    for p in shape:
        shape_indices.append(add_point(p, points, point_indices))
    return shape_indices

def kagome_strip(rows, cols, size):
    points = []
    edges = []
    point_indices = {}

    for row in range(rows):
        row_hexagons = []
        for col in range(cols):
            center = (col * 2 * size, row * np.sqrt(3) * size)
            hex_points, top_triangle, bottom_triangle = hexagon(center, size)
            hex_indices = []
            for shape in [hex_points, top_triangle, bottom_triangle]:
                shape_indices = create_shape(points, point_indices, shape)
                for i in range(len(shape_indices)):
                    edges.append((shape_indices[i], shape_indices[(i + 1) % len(shape_indices)]))
                hex_indices.append(shape_indices)
            row_hexagons.append(hex_indices)

        for col in range(cols - 1):
            current_hex = row_hexagons[col]
            next_hex = row_hexagons[col + 1]
            edges.append((current_hex[0][1], next_hex[0][2]))
            edges.append((current_hex[0][4], next_hex[0][5]))
    return points, edges

def linear_chain(num_points, size):
    points = []
    edges = []
    point_indices = {}
    for i in range(num_points):
        point = (i * size, 0)
        point_index = add_point(point, points, point_indices)
        if i > 0:
            edges.append((i - 1, i))

    return points, edges

kagome_cols = 3
chain_points = 11
size = 0.75
kagome_points, kagome_edges = kagome_strip(1, kagome_cols, 1)
chain_points, chain_edges = linear_chain(chain_points, size)

plt.figure(figsize=(15, 5))
base_colors = ['orange', 'red', 'yellow', 'green', 'cyan', 'blue', 'purple', 'violet', 'magenta', 'teal', 'pink', 'orange', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'magenta']
color_array = base_colors + ['black'] * 17

# Plot Kagome strip on the left side
for edge in kagome_edges:
    point1, point2 = edge
    x_values = [kagome_points[point1][0], kagome_points[point2][0]]
    y_values = [kagome_points[point1][1], kagome_points[point2][1]]
    plt.plot(x_values, y_values, 'k-')
i = 0
# Plot points for Kagome strip
for point, index in zip(kagome_points, range(1, len(kagome_points) + 1)):
    diameter_size = 50
    color = 'black'
    plt.scatter(point[0], point[1], color=color_array[i], marker='o', s=abs(diameter_size), zorder=2)
    i += 1
i = 0

# Plot linear chain on the right side
for edge in chain_edges:
    point1, point2 = edge
    x_values = [chain_points[point1][0] + kagome_cols * 2, chain_points[point2][0] + kagome_cols * 2]
    y_values = [chain_points[point1][1], chain_points[point2][1]]
    plt.plot(x_values, y_values, 'k-')

# Plot points for linear chain
for point, index in zip(chain_points, range(1, len(chain_points) + 1)):
    diameter_size = 50
    color = 'black'
    plt.scatter(point[0] + kagome_cols * 2, point[1], color=color_array[i], marker='o', s=abs(diameter_size), zorder=2)
    i += 1
last_point = chain_points[-1]

red_point_index = base_colors.index('red')
red_point = chain_points[red_point_index]

orange_point_index = base_colors.index('orange')
yellow_point_index = base_colors.index('yellow')
purple_point_index = base_colors.index('purple')
pink_point_index = base_colors.index('pink')

orange_point = chain_points[orange_point_index]
yellow_point = chain_points[yellow_point_index]
purple_point = chain_points[purple_point_index]
pink_point = chain_points[pink_point_index]

x_offset = kagome_cols * 2

def add_arrow(start, end, color):
    arrow = FancyArrowPatch((start[0] + x_offset, start[1]), (end[0] + x_offset, end[1]),
                            connectionstyle='arc3,rad=.5', color=color,
                            arrowstyle='->', mutation_scale=15)
    plt.gca().add_patch(arrow)

add_arrow(red_point, orange_point, 'black')
add_arrow(red_point, yellow_point, 'black')
add_arrow(red_point, purple_point, 'black')
add_arrow(red_point, pink_point, 'black')


plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
#plt.show()

plt.savefig('map_kagome.png', transparent = True)
plt.show()

image_path = 'map_kagome.png'
image = Image.open(image_path)
bbox = image.getbbox()
cropped_image = image.crop(bbox)
cropped_image_path = 'cropped.png'
cropped_image.save(cropped_image_path)