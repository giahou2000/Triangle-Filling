import numpy as np
import statistics
import interpolate_color as interpol


def shade_triangle(img, verts2d, vcolors, shade_t):
    """
    img: the canvas in which the new triangle will be stored
    verts2d: the 3 peaks of the triangle
    vcolors: the RGB colors of the 3 peaks
    shade_t: the painting method (flat or gouraud)
    """
    # the value to be returned - the canvas

    global right_color

    # find the minimums and maximums for each acme
    # we define acmes by their number (0, 1, 2)
    # acme 0 has peaks 0 and 1
    # acme 1 has peaks 1 and 2
    # acme 2 has peaks 2 and 0
    verts2d = np.array(verts2d)
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

    # _____*****if we are using flat method*****_____
    if shade_t == 'flat':
        # flat coloring for the whole triangle
        color = np.zeros(3)
        for i in range(3):
            i_color_palette = [vcolors[0][i], vcolors[1][i], vcolors[2][i]]
            color[i] = statistics.mean(i_color_palette)
            color = np.array(color)

        # if the triangle is a single point
        if (xmin == xmax) and (ymin == ymax):
            img[ymin][xmin] = color

        # if the triangle is a horizontal line
        elif ymin == ymax:
            a = 1
            for x in range(xmin, xmax+1):
                img[ymin][x] = color

        # if the triangle is a vertical line
        elif xmin == xmax:
            a = 1
            for y in range(ymin, ymax+1):
                img[y][xmin] = color

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
                    img[y][x] = color
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
                    img[y][x] = color
                xsmall = (y + 1 - ymax) * left_slope + peaks_y_max[0][0]
                xbig = (y + 1 - ymax) * right_slope + peaks_y_max[1][0]

        # if the triangle is just any other triangle
        # split it in two triangles and call the shade_triangle (itself)
        # note: we give the same color to each three peaks now because the mean value of the three colors will be the same color again
        else:
            # compute the x at which there will be the cut
            y_diff = peaks_y_max[0][0]-activ_peaks[0][0]
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
            shade_triangle(img, triangle1, colors, shade_t)
            # fill second triangle
            shade_triangle(img, triangle2, colors, shade_t)




    # _____*****if we are using gouraud method*****_____
    elif shade_t == 'gouraud':

        # if the triangle is a single point
        if (xmin == xmax) and (ymin == ymax):
            img[ymin][xmin] = vcolors[0]

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
                img[ymin][x] = interpol.interpolate_color(left_peak, right_peak, [x, ymin], left_color, right_color)

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
                img[y][xmin] = interpol.interpolate_color(down_peak, up_peak, [xmin, y], lower_color, upper_color)

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
                color1 = interpol.interpolate_color(activ_peaks[0], peaks_y_max[0], [xsmall, y], left_color, upper_color)
                color2 = interpol.interpolate_color(activ_peaks[1], peaks_y_max[0], [xbig, y], right_color, upper_color)
                for x in range(int(xsmall), int(xbig + 1)):
                    img[y][x] = interpol.interpolate_color([xsmall, y], [xbig, y], [x, y], color1, color2)
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
                color1 = interpol.interpolate_color(peaks_y_max[0], activ_peaks[0], [xsmall, y], left_color, down_color)
                color2 = interpol.interpolate_color(peaks_y_max[1], activ_peaks[0], [xbig, y], right_color, down_color)
                for x in range(int(xsmall), int(xbig + 1)):
                    img[y][x] = interpol.interpolate_color([xsmall, y], [xbig, y], [x, y], color1, color2)
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
            new_color = interpol.interpolate_color(peaks_y_max[0], activ_peaks[0], new_peak, upper_color, down_color)
            colors1 = [upper_color, middle_color, new_color]
            colors2 = [middle_color, new_color, down_color]
            # fill first triangle
            shade_triangle(img, triangle1, colors1, shade_t)
            # fill second triangle
            shade_triangle(img, triangle2, colors2, shade_t)

    return img
