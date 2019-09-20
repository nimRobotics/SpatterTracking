import cv2
import numpy as np
import glob

img_array = []
for i in range(200):
    img = cv2.imread("blob/BB_"+str(i)+".png")
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print(i)

# last second param is the fps
out = cv2.VideoWriter('out.avi',cv2.VideoWriter_fourcc(*'DIVX'), 20, size)

for i in range(len(img_array)):
    out.write(img_array[i])

out.release()
