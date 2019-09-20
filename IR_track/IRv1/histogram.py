import cv2
import numpy as np
from matplotlib import pyplot as plt
# https://youtu.be/mnmjZOLjoBA

# cv2.imread()
# second argument is a flag which specifies the way image should be read.
# (1) - cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
# (0) - cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
# (-1) - cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel

img = cv2.imread('1.png',0)
# numpy.ravel() returns a 1-D linear array
plt.hist(img.ravel(),256,[0,256])
plt.show()
