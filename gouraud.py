import numpy as np
import statistics
import interpolate_vector as interpol

def Gourauds(canvas, vertices, vcolors):
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


    # if the triangle is a single point
    if (xmin == xmax) and (ymin == ymax):
        canvas[ymin][xmin] = vcolors[0]

    # if the triangle is a horizontal line
    elif ymin == ymax:
        for i in range(3):
            if verts2d[i][0] == xmin:
                left_color = vcolors[i]
                left_peak = verts2d[i]
            elif verts2d[i][0] == xmax:
                right_color = vcolors[i]
                right_peak = verts2d[i]
        for x in range(xmin, xmax + 1):
            canvas[ymin][x] = interpol.interpolate_vectors(left_peak, right_peak, [x, ymin], left_color, right_color)

    # if the triangle is a vertical line
    elif xmin == xmax:
        for i in range(3):
            if verts2d[i][1] == ymax:
                upper_color = vcolors[i]
                up_peak = verts2d[i]
            elif verts2d[i][1] == ymin:
                lower_color = vcolors[i]
                down_peak = verts2d[i]
        for y in range(ymin, ymax + 1):
            canvas[y][xmin] = interpol.interpolate_vectors(down_peak, up_peak, [xmin, y], lower_color, upper_color)

    # if the triangle has a lower horizontal edge
    elif len(activ_peaks) == 2:
        # sort to left and right lower peaks
        activ_peaks.sort(key=lambda ap: ap[0])
        # compute the 2 slopes of the edges (inverse slopes to get rid of division by zero and simplify things)
        left_slope = (peaks_y_max[0][0] - activ_peaks[0][0])/(peaks_y_max[0][1] - activ_peaks[0][1])
        right_slope = (activ_peaks[1][0] - peaks_y_max[0][0])/(activ_peaks[1][1] - peaks_y_max[0][1])
        # find the right color for the right peak
        for i in range(3):
            if (verts2d[i][0] == activ_peaks[0][0]) and (verts2d[i][1] == ymin):
                left_color = vcolors[i]
            elif (verts2d[i][0] == activ_peaks[1][0]) and (verts2d[i][1] == ymin):
                right_color = vcolors[i]
            else:
                upper_color = vcolors[i]
        # paint for each point
        xsmall = activ_peaks[0][0]
        xbig = activ_peaks[1][0]
        for y in range(ymin, ymax + 1):
            color1 = interpol.interpolate_vectors(activ_peaks[0], peaks_y_max[0], [xsmall, y], left_color, upper_color)
            color2 = interpol.interpolate_vectors(activ_peaks[1], peaks_y_max[0], [xbig, y], right_color, upper_color)
            for x in range(int(xsmall), int(xbig + 1)):
                canvas[y][x] = interpol.interpolate_vectors([xsmall, y], [xbig, y], [x, y], color1, color2)
            xsmall = (y + 1 - ymin) * left_slope + activ_peaks[0][0]
            xbig = (y + 1 - ymin) * right_slope + activ_peaks[1][0]

    # if the triangle has an upper horizontal edge
    elif len(peaks_y_max) == 2:
        # sort to left and right lower peaks
        peaks_y_max.sort(key=lambda ap: ap[0])
        # compute the 2 slopes of the acmes (inverse slopes to get rid of division by zero)
        left_slope = (peaks_y_max[0][0] - activ_peaks[0][0])/(peaks_y_max[0][1] - activ_peaks[0][1])
        right_slope = (activ_peaks[0][0] - peaks_y_max[1][0])/(activ_peaks[0][1] - peaks_y_max[1][1])
        # find the right color for the right peak
        for i in range(3):
            if (verts2d[i][0] == peaks_y_max[0][0]) and (verts2d[i][1] == ymax):
                left_color = vcolors[i]
            elif (verts2d[i][0] == peaks_y_max[1][0]) and (verts2d[i][1] == ymax):
                right_color = vcolors[i]
            else:
                down_color = vcolors[i]
                xsmall = verts2d[i][0]
        # paint for each point
        xsmall = activ_peaks[0][0]
        xbig = xsmall
        for y in range(ymin, ymax + 1):
            color1 = interpol.interpolate_vectors(peaks_y_max[0], activ_peaks[0], [xsmall, y], left_color, down_color)
            color2 = interpol.interpolate_vectors(peaks_y_max[1], activ_peaks[0], [xbig, y], right_color, down_color)
            for x in range(int(xsmall), int(xbig + 1)):
                canvas[y][x] = interpol.interpolate_vectors([xsmall, y], [xbig, y], [x, y], color1, color2)
            xsmall = (y + 1 - ymax) * left_slope + peaks_y_max[0][0]
            xbig = (y + 1 - ymax) * right_slope + peaks_y_max[1][0]

    # if the triangle is just any other triangle
    else:
        # compute the x at which there will be the cut
        y_diff = peaks_y_max[0][0] - activ_peaks[0][0]
        slope = 0
        if y_diff == 0:
            x_new = peaks_y_max[0][0]
        else:
            slope = (ymax-ymin)/y_diff
            x_new = peaks_y_max[0][0] + (middle_peak[1] - ymax)/slope
        # the new cut peak
        new_peak = [x_new, middle_peak[1]]
        # create the new triangles after the cut
        # compute the colors
        for i in range(3):
            if (verts2d[i][1] == ymax):
                upper_color = vcolors[i]
            elif (verts2d[i][1] == ymin):
                down_color = vcolors[i]
            else:
                middle_color = vcolors[i]
        new_peak = [x_new, middle_peak[1]]
        # create the new triangles after the cut
        triangle1 = np.array([peaks_y_max[0], middle_peak, new_peak])
        triangle2 = np.array([middle_peak, new_peak, activ_peaks[0]])
        new_color = interpol.interpolate_vectors(peaks_y_max[0], activ_peaks[0], new_peak, upper_color, down_color)
        colors1 = [upper_color, middle_color, new_color]
        colors2 = [middle_color, new_color, down_color]
        # fill first triangle
        canvas = Gourauds(canvas, triangle1, colors1)
        # fill second triangle
        canvas = Gourauds(canvas, triangle2, colors2)
    return canvas