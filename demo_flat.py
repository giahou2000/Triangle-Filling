import cv2
import numpy as np
import render
import matplotlib.pyplot

# load the data of the image
data = np.load('C:/Users/Christos/chris/auth/Computer_graphics/pythonTriangleFill/hw1.npy', allow_pickle=True)
verts2d = data[()]['verts2d']
vcolors = data[()]['vcolors']
faces = data[()]['faces']
depth = data[()]['depth']

# render the image
image = render.render(verts2d, faces, vcolors, depth, 'flat')
matplotlib.pyplot.imshow(image)
matplotlib.pyplot.savefig('flat.png')
matplotlib.pyplot.show()
