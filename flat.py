import numpy as np
import statistics
import interpolate_vector as interpol

def flats(canvas, vertices, vcolors):
    """
    canvas: the canvas in which the new triangle will be stored
    vertices: the 3 peaks of the triangle
    vcolors: the RGB colors of the 3 peaks
    """
    global right_color
    # find the minimums and maximums for each acme
    # we define acmes by their number (0, 1, 2)
    # acme 0 has peaks 0 and 1
    # acme 1 has peaks 1 and 2
    # acme 2 has peaks 2 and 0
    verts2d = np.array(vertices)
    xkmin = np.zeros(3)
    xkmax = np.zeros(3)
    ykmin = np.zeros(3)
    ykmax = np.zeros(3)
    for k in range(3):
        xkmin[k] = min(verts2d[k][0], verts2d[(k + 1) % 3][0])
        xkmax[k] = max(verts2d[k][0], verts2d[(k + 1) % 3][0])
        ykmin[k] = min(verts2d[k][1], verts2d[(k + 1) % 3][1])
        ykmax[k] = max(verts2d[k][1], verts2d[(k + 1) % 3][1])
    ymin = int(min(ykmin))
    ymax = int(max(ykmax))
    xmin = int(min(xkmin))
    xmax = int(max(xkmax))

    # find the active peaks and keep some more info for later processing
    activ_peaks = []
    peaks_y_max = []
    middle_peak = []
    for i in range(3):
        # store the active peaks for ymin
        if verts2d[i][1] == ymin:
            activ_peaks.append(verts2d[i])
        # store the peaks for ymax
        elif verts2d[i][1] == ymax:
            peaks_y_max.append(verts2d[i])
        else:
            middle_peak = verts2d[i]

    # flat coloring for the whole triangle
    color = np.zeros(3)
    for i in range(3):
        i_color_palette = [vcolors[0][i], vcolors[1][i], vcolors[2][i]]
        color[i] = statistics.mean(i_color_palette)
        color = np.array(color)

    # if the triangle is a single point
    if (xmin == xmax) and (ymin == ymax):
        canvas[ymin][xmin] = color

    # if the triangle is a horizontal line
    elif ymin == ymax:
        for x in range(xmin, xmax+1):
            canvas[ymin][x] = color

    # if the triangle is a vertical line
    elif xmin == xmax:
        for y in range(ymin, ymax+1):
            canvas[y][xmin] = color

    # if the triangle has a lower horizontal edge
    elif len(activ_peaks) == 2:
        # sort to left and right lower peaks
        activ_peaks.sort(key=lambda ap: ap[0])
        # compute the 2 slopes of the acmes (inverse slopes to get rid of division by zero)
        left_slope = (peaks_y_max[0][0] - activ_peaks[0][0])/(ymax - ymin)
        right_slope = (activ_peaks[1][0] - peaks_y_max[0][0])/(ymin - ymax)
        # paint for each point
        xsmall = activ_peaks[0][0]
        xbig = activ_peaks[1][0]
        for y in range(ymin, ymax + 1):
            for x in range(int(xsmall), int(xbig + 1)):
                canvas[y][x] = color
            xsmall = (y + 1 - ymin) * left_slope + activ_peaks[0][0]
            xbig = (y + 1 - ymin) * right_slope + activ_peaks[1][0]

    # if the triangle has an upper horizontal edge
    elif len(peaks_y_max) == 2:
        # sort to left and right upper peaks
        peaks_y_max.sort(key=lambda ap: ap[0])
        # compute the 2 slopes of the acmes (inverse slopes to get rid of division by zero)
        left_slope = (activ_peaks[0][0] - peaks_y_max[0][0])/(ymin - ymax)
        right_slope = (peaks_y_max[1][0] - activ_peaks[0][0])/(ymax - ymin)
        # paint for each point
        xsmall = activ_peaks[0][0]
        xbig = activ_peaks[0][0]
        for y in range(ymin, ymax + 1):
            for x in range(int(xsmall), int(xbig + 1)):
                canvas[y][x] = color
            xsmall = (y + 1 - ymax) * left_slope + peaks_y_max[0][0]
            xbig = (y + 1 - ymax) * right_slope + peaks_y_max[1][0]

    # if the triangle is just any other triangle
    # split it in two triangles and call the shade_triangle (itself)
    # note: we give the same color to each three peaks now because the mean value of the three colors will be the same color again
    else:
        # compute the x at which there will be the cut
        y_diff = peaks_y_max[0][0] - activ_peaks[0][0]
        if y_diff == 0:
            x_new = peaks_y_max[0][0]
        else:
            slope = (ymax-ymin)/y_diff
            x_new = peaks_y_max[0][0] + (middle_peak[1] - ymax)/slope
        # the mean value of the same color is the color itself, so we give each peak the same color
        colors = np.array([color, color, color])
        new_peak = [x_new, middle_peak[1]]
        # create the new triangles after the cut
        triangle1 = np.array([peaks_y_max[0], middle_peak, new_peak])
        triangle2 = np.array([middle_peak, new_peak, activ_peaks[0]])
        # fill first triangle
        canvas = flats(canvas, triangle1, colors)
        # fill second triangle
        canvas = flats(canvas, triangle2, colors)
    return canvas