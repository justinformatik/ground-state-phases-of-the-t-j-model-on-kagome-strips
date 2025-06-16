import matplotlib.pyplot as plt
import numpy as np
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

points, edges = kagome_strip(1, 7, 1) # adjust number of stars, which is 3 right now.

plt.figure(figsize=(15, 5))
for point, index in zip(points, range(1, len(points) + 1)):
    diameter_size = 50
    color = 'black'
    plt.scatter(point[0], point[1], color=color, marker='o', s=abs(diameter_size), zorder=2)

# Select points to connect
selected_points_indices = [19, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 19, 9, 14, 10, 14, 12, 15, 13, 15]

for edge in edges:
    point1, point2 = edge
    x_values = [points[point1][0], points[point2][0]]
    y_values = [points[point1][1], points[point2][1]]

    plt.plot(x_values, y_values, 'k-', color='black')

for i in range(0, len(selected_points_indices), 2):
    point1 = selected_points_indices[i]
    point2 = selected_points_indices[i + 1]
    x_values = [points[point1][0], points[point2][0]]
    y_values = [points[point1][1], points[point2][1]]
    plt.scatter(x_values, y_values, color='red', marker='o', s=abs(diameter_size), zorder=2)
    plt.plot(x_values, y_values, 'r-', color='red')

plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')

plt.savefig('kagome_star.png', transparent = True)
plt.show()

image_path = 'kagome_star.png'
image = Image.open(image_path)
bbox = image.getbbox()
cropped_image = image.crop(bbox)
cropped_image_path = 'kagome_star.png'
cropped_image.save(cropped_image_path)