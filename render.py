import numpy as np
import shade_triangle as shade
import statistics as stats


def render(verts2d, faces, vcolors, depth, shade_t):

    # initiate the image
    M = 512
    N = 512
    img = np.ones((M, N, 3))

    # find the triangles' depths
    k = len(faces)
    print('The image has ')
    print(k)
    print('triangles')
    tri_depths = np.zeros(k)
    for i in range(k):
        depths = [depth[faces[i][0]], depth[faces[i][1]], depth[faces[i][2]]]
        tri_depths[i] = stats.mean(depths)

    # sort the depths and keep the indices' changes
    indices = np.argsort(tri_depths)

    # paint the triangles
    for i in reversed(range(k)):
        tri_face = faces[indices[i]]
        verts = [verts2d[tri_face[0]], verts2d[tri_face[1]], verts2d[tri_face[2]]]
        color = [vcolors[tri_face[0]], vcolors[tri_face[1]], vcolors[tri_face[2]]]
        img = shade.shade_triangle(img, verts, color, shade_t)
    # return the RGB values
    return img
