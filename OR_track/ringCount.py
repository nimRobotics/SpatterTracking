import numpy as np
import cv2
import math
from itertools import groupby

def circles(k):
    print("Processing frame ",k)
    img = cv2.imread('cluster/KM_'+str(k)+'.png')

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    x = []
    y = []
    r = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area>5:
            (X,Y),radius = cv2.minEnclosingCircle(contour)
            center = (int(X),int(Y))
            radius = int(radius)
            # cv2.circle(img,center,radius,(0,255,0),1)
            x.append(center[0])
            y.append(center[1])
            r.append(radius)

    repeat = []
    # find interior circles
    # https://doubleroot.in/lessons/circle/relative-postion-of-two-circles/
    for i in range(len(r)):
        for j in range(len(r)):
            if i!=j:
                c1c2 = ((x[i]-x[j])**2 + (y[i]-y[j])**2)**0.5
                r1r2 = abs(r[i]-r[j])
                if c1c2 <= r1r2 :
                    if r[i]>r[j]:
                        repeat.append(j)
                    else:
                        repeat.append(i)

    # remove interior circles
    for ele in sorted(list(set(repeat)), reverse = True):
        del r[ele]
        del x[ele]
        del y[ele]
    # # delete the largest circle i.e. plume region
    # maxpos = r.index(max(r))
    # r.pop(maxpos)
    # x.pop(maxpos)
    # y.pop(maxpos)

    # remove ones
    ones = [i for i,val in enumerate(r) if val==1]
    for ele in sorted(list(set(ones)), reverse = True):
        del r[ele]
        del x[ele]
        del y[ele]

    # print(len(r))
    # draw Circles
    for i in range(len(r)):
        cv2.circle(img,(x[i],y[i]),r[i],(0,255,0),1)
    return(r,x,y)
    # cv2.imwrite("blob/BB_"+str(k)+".png",img)

# imgFrame = cv2.imread('thresh/TH_1.png')
# # reference distance line
# cv2.line(imgFrame, (10,10),(40,10),(0, 255, 0), 1)
# # ring with plume as center
# cv2.circle(imgFrame, (519,787),170, (0, 255, 0), 1)
# cv2.imwrite("temp.jpg",imgFrame)

rOld,xOld,yOld = circles(0)
r = []
for i in range(1,200):
    rNew,xNew,yNew = circles(i)

    for n in range(len(rNew)):
        for o in range(len(rOld)):
            # distance from the ring center old frame
            distOld = ((519-xOld[o])**2 + (787-yOld[o])**2)**0.5
            # distance from the ring center new frame
            distNew = ((519-xNew[n])**2 + (787-yNew[n])**2)**0.5
            # distance between particles in two frames
            dist = ((xNew[n]-xOld[o])**2 + (yNew[n]-yOld[o])**2)**0.5

            if distOld < 185 and distNew > 185 and dist <35:
                r.append(rNew[n])
    # updation
    del rOld, xOld, yOld
    rOld = rNew
    xOld = xNew
    yOld = yNew
    del rNew, xNew, yNew
    # removal of zeros and consecutive repetions
    out  = [x[0] for x in groupby(list(filter((0).__ne__, r)))]
    print(out)
    print(len(out))
