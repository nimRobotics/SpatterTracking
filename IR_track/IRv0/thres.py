import cv2
import numpy as np

threshold = 114 # value set by hit and trial
# threshold = 15 # without IR filter
for i in range(200):
    print("Processing frame ",i)
    img = cv2.imread('cluster/KM_'+str(i)+'.png',0)
    ret,thresh1 = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
    cv2.imwrite("thresh/TH_"+str(i)+".png",thresh1)
