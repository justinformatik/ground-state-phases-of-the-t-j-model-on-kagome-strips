import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image

fig, ax = plt.subplots()
# hide
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_yticklabels([])
ax.set_yticks([])

ax.set_xlim(0, 4)
ax.set_ylim(0, 0.1) 
ax.set_xlabel('J', fontsize='x-large')

vertical_lines = [1.68, 3.25]
labels = [r'$\Delta$', 'P']
colors = sns.color_palette('colorblind', 3)
label_x_positions = [1.68, 3.25] 

line_height = 0.025

ymin = (0 - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
ymax = (line_height - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])

for vline, label, color, label_x in zip(vertical_lines, labels, colors, label_x_positions):
    if label == 'P':
        vline_start = vline - 0.25
        vline_end = vline + 0.25
        ax.fill_betweenx([0, line_height], vline_start, vline_end, color=color, alpha=0.2)
    elif label == r'$\Delta$':
        vline_start = vline - 0.2
        vline_end = vline + 0.2
        ax.fill_betweenx([0, line_height], vline_start, vline_end, color=color, alpha=0.2)
    

    ax.axvline(x=vline, ymin=ymin, ymax=ymax, color=color, linestyle='-', alpha=0.7)
    
    ax.text(label_x, 0.035, label, verticalalignment='top', horizontalalignment='center', fontsize=20)#label

plt.savefig('phasediagram1.png', transparent=True, dpi=500)
plt.show()

image_path = 'phasediagram1.png'
image = Image.open(image_path)
bbox = image.getbbox()
cropped_image = image.crop(bbox)
cropped_image_path = 'cropped.png'
cropped_image.save(cropped_image_path)