import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

x = np.linspace(-10, 10, 4000)
y = np.sin(x) + np.sin(3 * x / 2) * 0.5 + np.sin(5 * x / 3) * 0.2

dy = np.gradient(y, x)
local_minima_indices = np.where((np.roll(dy, 1) < 0) & (dy > 0))[0]

plt.figure(figsize=(12, 6))
plt.plot(x, y, color='black')
plt.scatter(x[local_minima_indices], y[local_minima_indices], color='red', zorder=5)

plt.text(x[local_minima_indices[2]], y[local_minima_indices][2]-0.25, r'$x_2$', fontsize=20)
plt.text(x[local_minima_indices[3]], y[local_minima_indices][3]-0.25, r'$x_1$', fontsize=20)

plt.gca().set_axis_off()
#plt.show()
plt.savefig('localMinimum.png', transparent=True, bbox_inches='tight', pad_inches=0)

image_path = 'localMinimum.png'
image = Image.open(image_path)
bbox = image.getbbox()
cropped_image = image.crop(bbox)
cropped_image_path = 'localMinimum_cropped.png'
cropped_image.save(cropped_image_path)

cropped_image.show()