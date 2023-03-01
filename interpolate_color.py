import numpy as np
import math

def interpolate_color(x1, x2, x, c1: np.array, c2: np.array):
    """
    ___3D point RGB color interpolation function___
    x1: first 3D point
    x2: second 3D point
    x: point at which we will compute the interpolation
    c1: x1's RGB color
    c2: x2's RGB color
    """
    # difference between the 2 points
    diff1 = abs(x2[0] - x1[0]) # x axis fifference
    diff2 = abs(x2[1] - x1[1]) # y axis difference
    # if the two points are the same(x1 == x2)
    if (diff1 == 0) and (diff2 == 0):
        value = 0.5 * c1 + 0.5 * c2
    # if the 2 points are different
    else:
        d1 = math.sqrt((x1[0]-x[0])**2 + (x1[1]-x[1])**2)
        d2 = math.sqrt((x2[0]-x[0])**2 + (x2[1]-x[1])**2)
        norm_pos = d1/(d1+d2)
        # the result from the interpolation
        value = (1 - norm_pos) * c1 + norm_pos * c2
    return value
