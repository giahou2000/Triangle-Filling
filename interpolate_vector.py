import numpy as np
import math

def interpolate_vectors(p1, p2, xy, V1: np.array, V2: np.array):
    """
    ___3D point RGB color interpolation function___
    p1: first 3D point
    p2: second 3D point
    xy: point at which we will compute the interpolation
    V1: x1's RGB color
    V2: x2's RGB color
    dim: the dimension of p1, p2, xy
    """

    # difference between the 2 points
    diff1 = abs(p2[0] - p1[0]) # x axis fifference
    diff2 = abs(p2[1] - p1[1]) # y axis difference
    # if the two points are the same(x1 == x2)
    if (diff1 == 0) and (diff2 == 0):
        V = 0.5 * V1 + 0.5 * V2
    # if the 2 points are different
    else:
        d1 = math.sqrt((p1[0] - xy[0])**2 + (p1[1] - xy[1])**2)
        d2 = math.sqrt((p2[0] - xy[0])**2 + (p2[1] - xy[1])**2)
        norm_pos = d1/(d1+d2)
        # the result from the interpolation
        V = (1 - norm_pos) * V1 + norm_pos * V2
    return V
