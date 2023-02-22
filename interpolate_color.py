import numpy as np


def interpolate_color(x1, x2, x, c1, c2):
    diff = abs(x2 - x1)
    # if the two points are the same(x1 == x2)
    if diff == 0:
        value = 0.5 * c1 + 0.5 * c2
    # if the 2 points are different
    else:
        # normalized position of x between x1 and x2
        norm_pos = abs((x-x1)/(x2-x1))
        # the result from the interpolation
        value = norm_pos * c1 + (1-norm_pos) * c2
    return value
