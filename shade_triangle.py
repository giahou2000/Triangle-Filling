import numpy as np
import statistics
import interpolate_vector as interpol
import flat
import gouraud


def shade_triangle(img, verts2d, vcolors, shade_t):
    """
    img: the canvas in which the new triangle will be stored
    verts2d: the 3 peaks of the triangle
    vcolors: the RGB colors of the 3 peaks
    shade_t: the painting method (flat or gouraud)
    """
    if shade_t == 'flat':
        updatedcanvas = flat.flats(img, verts2d, vcolors)
    elif shade_t == 'gouraud':
        updatedcanvas = gouraud.Gourauds(img, verts2d, vcolors)
    
    return updatedcanvas
