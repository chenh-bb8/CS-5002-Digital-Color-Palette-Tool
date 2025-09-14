import matplotlib.pyplot as plt
import numpy as np
import colorsys

# Visualize Hue Gradient
hues = np.linspace(0, 1, 360)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

plt.imshow([colors], extent=[0, 360, 0, 10])
plt.title("Hue Gradient")
plt.xlabel("Hue (degrees)")
plt.show()
