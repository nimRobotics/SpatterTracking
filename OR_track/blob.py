import numpy as np
import cv2
import math

for k in range(200):
    print("Processing frame ",k)
    img = cv2.imread('cluster/KM_'+str(k)+'.png')

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(len(contours))
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

    # TODO: delete the plume region

    # remove ones
    ones = [i for i,val in enumerate(r) if val==1]
    for ele in sorted(list(set(ones)), reverse = True):
        del r[ele]
        del x[ele]
        del y[ele]

    print(len(r))
    # draw Circles
    for i in range(len(r)):
        cv2.circle(img,(x[i],y[i]),r[i],(0,255,0),1)
    # cv2.circle(img, (430,618), 170, (0, 0, 255), 1)
    print(r)
    print(x)
    print(y)

    ORimg = cv2.imread('frames/OR_'+str(k)+'.png')
    FGimg = cv2.imread('fg/FG_'+str(k)+'.png')
    out = np.concatenate((ORimg,FGimg,img), axis=1)
    cv2.imwrite("blob/BB_"+str(k)+".png",out)
