import numpy as np
import cv2
import math

for k in range(200):
    print("Processing frame ",k)
    img = cv2.imread('frames/IR_'+str(k)+'.png')
    cv2.circle(img, (430,618), 27, (0, 0, 255), 1)
    cv2.imwrite("circles/CS_"+str(k)+".png",img)
