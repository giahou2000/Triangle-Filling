import numpy as np
import render
import matplotlib.pyplot
import cv2

# load the data of the image
data = np.load('h1.npy', allow_pickle=True)
verts2d = data[()]['verts2d']
vcolors = data[()]['vcolors']
faces = data[()]['faces']
depth = data[()]['depth']

# render the image
image = render.render(verts2d, faces, vcolors, depth, 'gouraud')
image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
matplotlib.pyplot.imshow(image)
matplotlib.pyplot.savefig('gouraud.png')
matplotlib.pyplot.show()
