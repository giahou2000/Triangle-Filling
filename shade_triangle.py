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

    # find the active peaks
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
        # flat coloring
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
            for x in range(xmin, xmax+1):
                img[ymin][x] = color

        # if the triangle is a vertical line
        elif xmin == xmax:
            for y in range(ymin, ymax+1):
                img[y][xmin] = color

        # if the triangle has a lower horizontal edge
        elif len(activ_peaks) == 2:
            # sort to left and right lower peaks
            activ_peaks.sort(key=lambda ap: ap[0])
            left_slope = (peaks_y_max[0][0] - activ_peaks[0][0])/(ymax - ymin)
            right_slope = (activ_peaks[1][0] - peaks_y_max[0][0])/(ymin - ymax)
            for y in range(ymin, ymax + 1):
                for x in range(int(xmin), int(xmax + 1)):
                    img[y][x] = color
                xmin = xmin + left_slope
                xmax = xmax + right_slope

        # if the triangle has an upper horizontal edge
        elif len(peaks_y_max) == 2:
            peaks_y_max.sort(key=lambda ap: ap[0])
            left_slope = (activ_peaks[0][0] - peaks_y_max[0][0])/(ymin - ymax)
            right_slope = (peaks_y_max[1][0] - activ_peaks[0][0])/(ymax - ymin)
            for y in range(ymin, ymax + 1):
                for x in range(int(xmin), int(xmax + 1)):
                    img[y][x] = color
                xmin = xmin + left_slope
                xmax = xmax + right_slope

        # if the triangle is just any other triangle
        # split it in two triangles and call the shade_triangle (itself)
        # note: we give the same color to each three peaks now because the mean value of the three colors will be the same color again
        else:
            y_diff = peaks_y_max[0][0]-activ_peaks[0][0]
            if y_diff == 0:
                x_new = peaks_y_max[0][0]
            else:
                slope = (ymax-ymin)/y_diff
                x_new = peaks_y_max[0][0] + (middle_peak[1] - ymax)/slope
            colors = np.array([color, color, color])
            new_peak = [x_new, middle_peak[1]]
            triangle1 = np.array([peaks_y_max[0], middle_peak, new_peak])
            triangle2 = np.array([middle_peak, new_peak, activ_peaks[0]])
            # fill first triangle
            shade_triangle(img, triangle1, colors, shade_t)
            # fill second triangle
            shade_triangle(img, triangle2, colors, shade_t)




    # _____*****if we are using gouraud method*****_____
    elif shade_t == 'gouraud':
        a = 1
        # # if the triangle is a single point(no point of gouraud method)
        # if (xmin == xmax) and (ymin == ymax):
        #     color = np.zeros(3)
        #     for i in range(3):
        #         i_color_palette = [vcolors[0][i], vcolors[1][i], vcolors[2][i]]
        #         color[i] = statistics.mean(i_color_palette)
        #     Y[ymin][xmin] = color

        # # if the triangle is a horizontal line
        # elif ymin == ymax:
        #     for i in range(3):
        #         if activ_peaks_min[i][0] == xmin:
        #             left_color = vcolors[i]
        #         elif activ_peaks_min[i][0] == xmax:
        #             right_color = vcolors[i]
        #     for x in range(xmin, xmax + 1):
        #         Y[ymin][x] = interpol.interpolate_color(xmin, xmax, x, left_color, right_color)

        # # if the triangle is a vertical line
        # elif xmin == xmax:
        #     for i in range(3):
        #         if verts2d[i][1] == ymax:
        #             upper_color = vcolors[i]
        #         elif verts2d[i][1] == ymin:
        #             lower_color = vcolors[i]
        #     for y in range(ymin, ymax + 1):
        #         Y[y][xmin] = interpol.interpolate_color(ymin, ymax, y, lower_color, upper_color)

        # # if the triangle has a lower horizontal edge
        # elif len(activ_peaks_min) == 2:
        #     activ_peaks_min.sort(key=lambda ap: ap[0])
        #     for i in range(3):
        #         if verts2d[i][1] == ymax:
        #             upper_point = verts2d[i]
        #             upper_color = vcolors[i]
        #         elif verts2d[i][0] == activ_peaks_min[0][0]:
        #             left_color = vcolors[i]
        #         elif verts2d[i][0] == activ_peaks_min[1][0]:
        #             right_color = vcolors[i]
        #     left_slope = (upper_point[0] - activ_peaks_min[0][0]) / (upper_point[1] - activ_peaks_min[0][1])
        #     right_slope = (activ_peaks_min[1][0] - upper_point[0]) / (activ_peaks_min[1][1] - upper_point[1])
        #     for y in range(ymin, ymax + 1):
        #         # first interpolation
        #         left_side_color = interpol.interpolate_color(ymin, ymax, y, left_color, upper_color)
        #         right_side_color = interpol.interpolate_color(ymin, ymax, y, right_color, upper_color)
        #         left_x = int(activ_peaks_min[0][0])
        #         right_x = int(activ_peaks_min[1][0])
        #         for x in range(left_x, right_x + 1):
        #             # second interpolation
        #             Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #         new_left_x = round((y + 1 - ymin) * left_slope)
        #         new_right_x = round((y + 1 - ymin) * right_slope)
        #         activ_peaks_min[0] = [new_left_x, y + 1]
        #         activ_peaks_min[1] = [new_right_x, y + 1]

        # # if the triangle has an upper horizontal edge
        # elif len(activ_peaks_max) == 2:
        #     activ_peaks_max.sort(key=lambda ap: ap[0])
        #     for i in range(3):
        #         if verts2d[i][1] == ymin:
        #             lower_point = verts2d[i]
        #             lower_color = vcolors[i]
        #         elif verts2d[i][0] == activ_peaks_max[0][0]:
        #             left_color = vcolors[i]
        #         elif verts2d[i][0] == activ_peaks_max[1][0]:
        #             right_color = vcolors[i]
        #     left_slope = (activ_peaks_max[0][0] - lower_point[0]) / (activ_peaks_max[0][1] - lower_point[1])
        #     right_slope = (activ_peaks_max[1][0] - lower_point[0]) / (activ_peaks_max[1][1] - lower_point[1])
        #     activ_peaks_min.append(activ_peaks_min[0])
        #     for y in range(ymin, ymax + 1):
        #         # first interpolation
        #         left_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, left_color)
        #         right_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, right_color)
        #         left_x = int(activ_peaks_min[0][0])
        #         right_x = int(activ_peaks_min[1][0])
        #         for x in range(left_x, right_x + 1):
        #             # second interpolation
        #             Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #         new_left_x = round((y + 1 - ymin) * left_slope)
        #         new_right_x = round((y + 1 - ymin) * right_slope)
        #         activ_peaks_min[0] = [new_left_x, y + 1]
        #         activ_peaks_min[1] = [new_right_x, y + 1]

        # # if the triangle is just a triangle
        # else:
        #     # if the middle point is from the left side
        #     if middle_peak[0] == xmin:
        #         slope_left_1 = (xmin - activ_peaks_min[0][0]) / (middle_peak[1] - ymin)
        #         slope_left_2 = (activ_peaks_max[0][0] - xmin) / (ymax - middle_peak[1])
        #         slope_right = (activ_peaks_max[0][0] - activ_peaks_min[0][0]) / (ymax - ymin)
        #         # get the colors
        #         for i in range(3):
        #             if verts2d[i][1] == ymax:
        #                 upper_color = vcolors[i]
        #             elif verts2d[i][1] == ymin:
        #                 lower_color = vcolors[i]
        #             elif verts2d[i][1] == middle_peak[1]:
        #                 middle_color = vcolors[i]
        #         # the list of the first scan line
        #         activ_peaks_min.append(activ_peaks_min[0])
        #         for y in range(ymin, int(middle_peak[1])):
        #             # first interpolation
        #             left_side_color = interpol.interpolate_color(ymin, middle_peak[1], y, lower_color, middle_color)
        #             right_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, upper_color)
        #             left_x = int(activ_peaks_min[0][0])
        #             right_x = int(activ_peaks_min[1][0])
        #             for x in range(left_x, right_x + 1):
        #                 # second interpolation
        #                 Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #             new_x_left = round((y + 1 - ymin) * slope_left_1)
        #             new_x_right = round((y + 1 - ymin) * slope_right)
        #             activ_peaks_min[0] = [new_x_left, y + 1]
        #             activ_peaks_min[1] = [new_x_right, y + 1]
        #         for y in range(int(middle_peak[1]), ymax + 1):
        #             # first interpolation
        #             left_side_color = interpol.interpolate_color(middle_peak[1], ymax, y, middle_color, upper_color)
        #             right_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, upper_color)
        #             left_x = activ_peaks_min[0][0]
        #             right_x = activ_peaks_min[1][0]
        #             for x in range(left_x, right_x + 1):
        #                 # second interpolation
        #                 Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #             new_x_left = round((y + 1 - ymin) * slope_left_2)
        #             new_x_right = round((y + 1 - ymin) * slope_right)
        #             activ_peaks_min[0] = [new_x_left, y + 1]
        #             activ_peaks_min[1] = [new_x_right, y + 1]

        #     # if the middle point is from the right side
        #     if middle_peak[0] == xmax:
        #         slope_right_1 = (middle_peak[0] - activ_peaks_min[0][0]) / (middle_peak[1] - ymin)
        #         slope_right_2 = (activ_peaks_max[0][0] - middle_peak[0]) / (ymax - middle_peak[1])
        #         slope_left = (activ_peaks_max[0][0] - activ_peaks_min[0][0]) / (ymax - ymin)
        #         # get the colors
        #         for i in range(3):
        #             if verts2d[i][1] == ymax:
        #                 upper_color = vcolors[i]
        #             elif verts2d[i][1] == ymin:
        #                 lower_color = vcolors[i]
        #             elif verts2d[i][1] == middle_peak[1]:
        #                 middle_color = vcolors[i]
        #         # the list of the first scan line
        #         activ_peaks_min.append(activ_peaks_min[0])
        #         # scan
        #         for y in range(ymin, int(middle_peak[1])):
        #             # first interpolation
        #             left_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, upper_color)
        #             right_side_color = interpol.interpolate_color(ymin, middle_peak[1], y, lower_color, middle_color)
        #             left_x = int(activ_peaks_min[0][0])
        #             right_x = int(activ_peaks_min[1][0])
        #             for x in range(left_x, right_x + 1):
        #                 # second interpolation
        #                 Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #             new_x_left = round((y + 1 - ymin) * slope_right_1)
        #             new_x_right = round((y + 1 - ymin) * slope_left)
        #             activ_peaks_min[0] = [new_x_left, y + 1]
        #             activ_peaks_min[1] = [new_x_right, y + 1]
        #         for y in range(int(middle_peak[1]), ymax + 1):
        #             # first interpolation
        #             left_side_color = interpol.interpolate_color(ymin, ymax, y, lower_color, upper_color)
        #             right_side_color = interpol.interpolate_color(middle_peak[1], ymax, y, middle_color, upper_color)
        #             left_x = activ_peaks_min[0][0]
        #             right_x = activ_peaks_min[1][0]
        #             for x in range(left_x, right_x + 1):
        #                 # second interpolation
        #                 Y[y][x] = interpol.interpolate_color(left_x, right_x, x, left_side_color, right_side_color)
        #             new_x_left = round((y + 1 - ymin) * slope_right_2)
        #             new_x_right = round((y + 1 - ymin) * slope_left)
        #             activ_peaks_min[0] = [new_x_left, y + 1]
        #             activ_peaks_min[1] = [new_x_right, y + 1]

    return img
