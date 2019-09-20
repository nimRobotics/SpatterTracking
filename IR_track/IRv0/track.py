import numpy as np
import cv2
import math
from itertools import groupby

def circles(k):
    print("Processing frame ",k)
    img = cv2.imread('thresh/TH_'+str(k)+'.png')

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    x = []
    y = []
    r = []

    for contour in contours:
        # cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
        (X,Y),radius = cv2.minEnclosingCircle(contour)
        center = (int(X),int(Y))
        # condition to not include the particles near plume
        if ((center[0]-430)**2+(center[1]-618)**2)**0.5 > 40 and radius>1:
            x.append(center[0])
            y.append(center[1])
            r.append(radius)

    repeat = []
    # # find interior circles
    # # https://doubleroot.in/lessons/circle/relative-postion-of-two-circles/
    # for i in range(len(r)):
    #     for j in range(len(r)):
    #         if i!=j:
    #             c1c2 = ((x[i]-x[j])**2 + (y[i]-y[j])**2)**0.5
    #             r1r2 = abs(r[i]-r[j])
    #             if c1c2 <= r1r2 :
    #                 if r[i]>r[j]:
    #                     repeat.append(j)
    #                 else:
    #                     repeat.append(i)
    #
    # # remove interior circles
    # for ele in sorted(list(set(repeat)), reverse = True):
    #     del r[ele]
    #     del x[ele]
    #     del y[ele]

    # delete the largest circle i.e. plume region
    maxpos = r.index(max(r))
    r.pop(maxpos)
    x.pop(maxpos)
    y.pop(maxpos)

    # # remove ones
    # ones = [i for i,val in enumerate(r) if val==1]
    # for ele in sorted(list(set(ones)), reverse = True):
    #     del r[ele]
    #     del x[ele]
    #     del y[ele]

    # print(len(r))
    # draw Circles
    for i in range(len(r)):
        cv2.circle(img,(x[i],y[i]),int(r[i]),(0,255,0),1)
    cv2.circle(img, (430,618), 40, (0, 255, 0), 1)
    # cv2.imwrite("track/TK_"+str(k)+".png",img)
    return(r,x,y)

def angle(x1,x2,y1,y2):
    return(math.atan2(y2-y1,x2-x1))

def dist(x1,x2,y1,y2):
    return(((x2-x1)**2+(y2-y1)**2)**0.5)

def particleInit(i,j):
    r1,x1,y1 = circles(i)
    r2,x2,y2 = circles(j)
    # print(len(r1))

    for n in range(len(r2)):
        for o in range(len(r1)):
            distance = dist(x1[o],x2[n],y1[o],y2[n])
            if distance <10:
                theta = angle(x1[o],x2[n],y1[o],y2[n])
                part.append([[x1[o], y1[o] ,r1[o], distance, theta]])

part = []
particleInit(0,1)

# print(part)
# print(part[0])
# print(part[0][0])
# print(part[0][0][0])

for i in range(2,199):
    # particles in new frame
    rNew,xNew,yNew = circles(i)
    gindex=[]
    # print(rNew)
    for x in range(len(part)):
        # print(part[x])
        # print(part[x][len(part[x])-1][0])
        xpred = part[x][len(part[x])-1][0] + part[x][len(part[x])-1][3]*np.cos(part[x][len(part[x])-1][4])
        ypred = part[x][len(part[x])-1][1] + part[x][len(part[x])-1][3]*np.sin(part[x][len(part[x])-1][4])

        for g in range(len(rNew)):
            distance = dist(xpred,xNew[g],ypred,yNew[g])
            # add new position to existing particle if old particle is detected
            if distance<5:
                gindex.append(g)
                # d = ((xNew[n]-part[o][len(part[o])-1][0])**2 + (yNew[n]-part[o][len(part[o])-1][1])**2)**0.5
                d = dist(part[x][len(part[x])-1][0],xNew[g],part[x][len(part[x])-1][1],yNew[g])
                t = angle(part[x][len(part[x])-1][0],xNew[g],part[x][len(part[x])-1][1],yNew[g])
                part[x].append([xNew[g], yNew[g] ,rNew[g], d, t])

    for ele in sorted(list(set(gindex)), reverse = True):
        del rNew[ele]
        del xNew[ele]
        del yNew[ele]
    # print("unmatched r",rNew)
    # print("unmatched x",xNew)
    # print("unmatched y",yNew)

    nr,nx,ny = circles(i+1)
    for a in range(len(rNew)):
        for b in range(len(nr)):
            distance = dist(nx[b],xNew[a],ny[b],yNew[a])
            if distance<10:
                theta = angle(nx[b],xNew[a],ny[b],yNew[a])
                part.append([[xNew[a], yNew[a] ,rNew[a], distance, theta]])

    # print(len(part))
    imgFrame = cv2.imread("frames/IR_"+str(i)+".png")
    for k in range(len(part)):
        for j in range(len(part[k])-1):
            cv2.line(imgFrame, (part[k][j][0],part[k][j][1]),(part[k][j+1][0],part[k][j+1][1]),(0, 0, 255), 1)

    #cv2.imwrite("track/TK_"+str(i)+".png",imgFrame)

print(part)
print(len(part))
partIndex = []
for i in range(len(part)):
    if len(part[i])<5:
        partIndex.append(i)

for ele in sorted(list(set(partIndex)), reverse = True):
    del part[ele]
print(len(part))

imgFrame = cv2.imread('frames/IR_0.png')
for i in range(len(part)):
    for j in range(len(part[i])-1):
        cv2.line(imgFrame, (part[i][j][0],part[i][j][1]),(part[i][j+1][0],part[i][j+1][1]),(0, 0, 255), 1)

cv2.imwrite("outpdold.jpg",imgFrame)
