import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate_triangle_arrows_question_image(vertices, directions):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # triangle
    triangle = plt.Polygon(vertices, closed=True, edgecolor='black', facecolor='none')
    ax.add_patch(triangle)

    # Add arrows or a question mark at each vertex based on the directions
    for vertex, direction in zip(vertices, directions):
        x, y = vertex
        if direction == 'u':  # arrow up
            dx, dy = 0, 0.2
            y_start = y
        elif direction == 'd':  # arrow down
            dx, dy = 0, -0.2
            y_start = y
        else:
            continue  # skip, if not 'u' or 'd'
        
        ax.arrow(x, y_start, dx, dy, head_width=0.05, head_length=0.1, fc='black', ec='black')

    ax.set_xlim(min(v[0] for v in vertices) - 0.5, max(v[0] for v in vertices) + 0.5)
    ax.set_ylim(min(v[1] for v in vertices) - 0.5, max(v[1] for v in vertices) + 0.5)
    
    plt.savefig('triangle.png', bbox_inches='tight')
    #plt.show()

vertices = [[0, 0], [1, 0], [0.5, 0.866]]
directions = ['u', 'd', 'd'] 
generate_triangle_arrows_question_image(vertices, directions)