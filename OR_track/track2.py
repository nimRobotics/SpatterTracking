"""
Author: Aakash Yadav
"""
import numpy as np
import cv2
import math
from itertools import groupby
import matplotlib.pyplot as plt

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
        # cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
        (X,Y),radius = cv2.minEnclosingCircle(contour)
        center = (int(X),int(Y))
        # TODO: add contour area also
        # area=cv2.contourArea(contour)
        # condition to exclude the particles near plume
        if ((center[0]-519)**2+(center[1]-787)**2)**0.5 > 60 and radius>=2:
            x.append(center[0])
            y.append(center[1])
            r.append(int(radius))

    repeat = []  #store index of interior circles
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

    # # remove ones
    # ones = [i for i,val in enumerate(r) if val==1]
    # for ele in sorted(list(set(ones)), reverse = True):
    #     del r[ele]
    #     del x[ele]
    #     del y[ele]

    # print(len(r))
    # draw Circles
    # for i in range(len(r)):
    #     cv2.circle(img,(x[i],y[i]),r[i],(0,255,0),1)
    # cv2.circle(img, (430,618), 150, (0, 255, 0), 1)
    # cv2.imwrite("blob/BB_"+str(k)+".png",img)
    return(r,x,y)

def angle(x1,x2,y1,y2):
    return(math.atan2(y2-y1,x2-x1))

def dist(x1,x2,y1,y2):
    return(((x2-x1)**2+(y2-y1)**2)**0.5)

def particleInit(i,j):
    r1,x1,y1 = circles(i)
    r2,x2,y2 = circles(j)
    oindex=[]
    for n in range(len(r2)):
        distTemp =[]
        for o in range(len(r1)):
            distance = dist(x1[o],x2[n],y1[o],y2[n])
            if distance<16 and distance!=0 and abs(r1[o]-r2[n])<=5 and (o not in oindex):
                distTemp.append(distance)
        try:
            o = distTemp.index(min(distTemp))
            oindex.append(o)
            theta = angle(x1[o],x2[n],y1[o],y2[n])
            part.append([[x1[o],y1[o],r1[o],min(distTemp),theta]])
        except ValueError:
            print("undetected")

part = []
particleInit(0,1)

for i in range(2,199):
    # particles in new frame
    rNew,xNew,yNew = circles(i)
    gindex=[]
    for x in range(len(part)):
        # predicted cordinates
        xpred = part[x][len(part[x])-1][0] + part[x][len(part[x])-1][3]*np.cos(part[x][len(part[x])-1][4])
        ypred = part[x][len(part[x])-1][1] + part[x][len(part[x])-1][3]*np.sin(part[x][len(part[x])-1][4])
        for g in range(len(rNew)):
            # distance between predicted and actual postion
            distance = dist(xpred,xNew[g],ypred,yNew[g])
            # add new position to existing particle if old particle is detected
            if distance<5 and (g not in gindex):
                # noting the index of detected elements
                gindex.append(g)
                # distance and theta for old and new position
                d = dist(part[x][len(part[x])-1][0],xNew[g],part[x][len(part[x])-1][1],yNew[g])
                t = angle(part[x][len(part[x])-1][0],xNew[g],part[x][len(part[x])-1][1],yNew[g])
                part[x].append([xNew[g],yNew[g],rNew[g],d,t])
                break

    # remove all elements at gindex, the ones that remain are unmatched
    for ele in sorted(list(set(gindex)), reverse = True):
        del rNew[ele]
        del xNew[ele]
        del yNew[ele]

    # initializing the particle undetected in previous frames
    nr,nx,ny = circles(i+1)
    bindex=[]
    for a in range(len(rNew)):
        distTemp =[]
        for b in range(len(nr)):
            distance = dist(nx[b],xNew[a],ny[b],yNew[a])
            if distance<16 and distance!=0 and abs(rNew[a]-nr[b])<=5 and (b not in bindex):
                distTemp.append(distance)
                # radDiff.append(rNew[a]-nr[b])
        try:
            b = distTemp.index(min(distTemp))
            bindex.append(b)
            theta = angle(nx[b],xNew[a],ny[b],yNew[a])
            part.append([[xNew[a], yNew[a] ,rNew[a], min(distTemp), theta]])
        except ValueError:
            print("undetected")

    # print(part)
    # write each tracked frame to "/track"
    imgFrame = cv2.imread('cluster/KM_'+str(i)+'.png')
    for z in range(len(part)):
        for j in range(len(part[z])-1):
            cv2.line(imgFrame, (part[z][j][0],part[z][j][1]),(part[z][j+1][0],part[z][j+1][1]),(0, 0, 255), 1)
    cv2.imwrite("track2/TK_"+str(i)+".png",imgFrame)

# print(part)
# print(len(part))

# removing the short tracked paths
partIndex = []
for i in range(len(part)):
    if len(part[i])<6:
        partIndex.append(i)
for ele in sorted(list(set(partIndex)), reverse = True):
    del part[ele]
print(len(part))

# 30 fps video, time for 1 frame
time = 1/30
x_vel = []
y_vel = []
# writing the final frame
imgFrame = cv2.imread('frames/OR_0.png')
for i in range(len(part)):
    for j in range(len(part[i])-1):
        cv2.line(imgFrame, (part[i][j][0],part[i][j][1]),(part[i][j+1][0],part[i][j+1][1]),(0, 0, 255), 1)
        x_vel.append((part[i][j][0]-part[i][j+1][0])/time)
        y_vel.append((part[i][j][1]-part[i][j+1][1])/time)

cv2.imwrite("outpd2.jpg",imgFrame)
# plt.scatter(x_vel,y_vel,color=['red','green'])
# plt.xlabel("pixel units/s")
# plt.ylabel("pixel units/s")
# plt.legend()
# plt.show()
n, bins, patches = plt.hist(x_vel, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('velocity (pixel units/sec)')
plt.ylabel('Frequency')
plt.title('Velocity distribution in x-direction')
plt.show()
