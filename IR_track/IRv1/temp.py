import numpy as np
import cv2 as cv
import argparse

#
# cap = cv.VideoCapture("slow_traffic_small.mp4")
# # cap = cv.VideoCapture("method_2_forground.avi")
#
# # params for ShiTomasi corner detection
# feature_params = dict( maxCorners = 100,
#                        qualityLevel = 0.3,
#                        minDistance = 7,
#                        blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors for drawing tracks
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
old_frame = cv.imread("blob/BB_0.png")
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
# x[475, 462, 499, 796, 322, 466, 445, 436, 437, 532, 455, 521, 437, 498, 57, 727, 426, 498, 827, 421, 522, 635, 854]
# y[636, 626, 625, 621, 600, 599, 595, 590, 587, 583, 582, 567, 567, 560, 559, 557, 551, 541, 538, 536, 535, 528, 439]

p0 = np.array([[475 ,636] ,[462, 626] ,[499 ,625], [796, 621] ,[322 ,600], [466 ,599]])
print(p0)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

for z in range(1,199):
    frame = cv.imread("blob/BB_"+str(z)+".png")
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imwrite(str(z)+".png",frame_gray)

    # calculate optical flow
    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
