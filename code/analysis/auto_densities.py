# SPECIFY PATHS!
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

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

def plot_kagome(J_value, stars, base_path, output_path):
    points, edges = kagome_strip(1, stars, 1)

    plt.figure(figsize=(10, 5))
    for edge in edges:
        point1, point2 = edge
        x_values = [points[point1][0], points[point2][0]]
        y_values = [points[point1][1], points[point2][1]]
        plt.plot(x_values, y_values, 'k-')

    df = pd.read_csv(f'{base_path}/local_density_S0_{J_value}.csv')
    df2 = pd.read_csv(f'{base_path}/not_allowed_values_for_sites.csv')

    notallowed = df2['SiteAllowedNotAllowed'].values
    sites = df['Site']
    local_density = df['LocalDensity']

    adjusted_sites = []
    current_site = 1

    for site in df['Site']:
        while current_site in notallowed:
            current_site += 1
        adjusted_sites.append(current_site)
        current_site += 1

    adjusted_df = pd.DataFrame({'Site': adjusted_sites, 'LocalDensity': local_density})
    vertices = adjusted_df['Site']
    local_density_ad = adjusted_df['LocalDensity']

    for point, index in zip(points, range(1, len(points) + 1)):
        if index in vertices.values:
            diameter_size = local_density_ad[adjusted_df['Site'] == index].values[0]
            color = 'green'
            plt.scatter(point[0], point[1], color=color, marker='o', s=abs(diameter_size) * 1000, zorder=2) #1000 and 200 for 5 stars and 11 stars

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.savefig(f'{output_path}/5stars_local_density_S0_{J_value}.pgf', bbox_inches='tight', pad_inches=0.2)
    plt.show()
    plt.close()

def main():
    stars = 5  ###############
    base_path = '' #specify
    output_path = '' #speficy
    J_values = np.arange(0.0, 3.5, 0.5)

    for J in J_values:
        plot_kagome(J, stars, base_path, output_path)

main()