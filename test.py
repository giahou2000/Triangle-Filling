import matplotlib.pyplot
import numpy as np
M = 512
N = 512
img = np.ones((M, N, 3))
activ_peaks = []
a = [300, 250]
b = [320, 250]
c = [290, 270]
activ_peaks.append(a)
activ_peaks.append(b)
peaks_y_max = []
peaks_y_max.append(c)
ymin = 250
ymax = 270
xmin = 290
xmax = 320
color = [0.8, 0.7, 0.9]

# sort to left and right lower peaks
activ_peaks.sort(key=lambda ap: ap[0])
# compute the 2 slopes of the acmes (inverse slopes to get rid of division by zero)
left_slope = (peaks_y_max[0][0] - activ_peaks[0][0])/(ymax - ymin)
right_slope = (activ_peaks[1][0] - peaks_y_max[0][0])/(ymin - ymax)
# paint for each point
for y in range(ymin, ymax + 1):
    for x in range(int(xmin), int(xmax + 1)):
        img[y][x] = color
    xmin = (y + 1 - ymin) * left_slope + activ_peaks[0][0]
    xmax = (y + 1 - ymin) * right_slope + activ_peaks[1][0]
    print(f"xmin= {xmin}")
    print(f"xmax= {xmax}")


matplotlib.pyplot.imshow(img, origin='lower')
matplotlib.pyplot.show()