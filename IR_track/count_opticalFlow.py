import cv2
import numpy as np

# return the single frame at the given index
def frameGen(frameIndex):
	# check for valid frame number
    if frameIndex >= 0 & frameIndex <= totalFrames:
    	# set frame position
    	cap.set(cv2.CAP_PROP_POS_FRAMES,frameIndex)
    else:
    	print("Error: frame index out of range")

    ret, frame = cap.read()
    # cv2.imwrite("frame"+str(frameIndex)+".jpg", frame)
    return(frame)

# returns local average bacground image for a given index
def bgCalc(i):
	# number of frames for calculating the average | odd val
	windowSize = 9
	# number if frame padded to the left and right of the index i
	padding = (windowSize-1)//2
	fgbg = cv2.createBackgroundSubtractorMOG2()
	if i<padding:
		for j in range(i+8):
			fgmask=fgbg.apply(frameGen(j),learningRate=0.2)
			# fgmask=cv2.BackgroundSubtractor.apply(image[, fgmask[, learningRate]])
			bgmask=fgbg.getBackgroundImage()

	elif i>=padding and i<=totalFrames-padding:
		for j in range(i-padding,i+padding):
			fgmask=fgbg.apply(frameGen(j),learningRate=0.2)
			# fgmask=cv2.BackgroundSubtractor.apply(image[, fgmask[, learningRate]])
			bgmask=fgbg.getBackgroundImage()
			# cv2.imwrite(str(j)+".jpg",bgmask)
			# cv2.imwrite("a"+str(j)+".jpg",fgmask)

	elif i>totalFrames-padding:
		for j in range(i-8,totalFrames):
			fgmask=fgbg.apply(frameGen(j),learningRate=0.2)
			# fgmask=cv2.BackgroundSubtractor.apply(image[, fgmask[, learningRate]])
			bgmask=fgbg.getBackgroundImage()
	else:
		print("Incorrect frame index")
	return(bgmask)

# identifies the particles in the frame and saves the labeled image
def circleIdentifier(i):
    imgFrame = frameGen(i)
    img = 2*(0.5*imgFrame-0.5*bgCalc(i))
    cv2.imwrite("out/kang"+str(i)+".jpg",img)
    img=cv2.imread("out/kang"+str(i)+".jpg",0)

    # adaptive mean thresholding
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

    # removing noise using kernel
    kernel = 2*np.ones((3,3),np.float32)
    median = cv2.filter2D(th2,-1,kernel)

    # HoughCircles method
    circles = cv2.HoughCircles(median, cv2.HOUGH_GRADIENT, 1, median.shape[0]/30, param1=60, param2=10,minRadius=5, maxRadius=20)
    return(circles,median)

    # # drawing the circles
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for k in circles[0, :]:
    #         center = (k[0], k[1])
    #         # circle center
    #         cv2.circle(imgFrame, center, 1, (0, 100, 100), 2)
    #         # circle outline
    #         radius = k[2]
    #         cv2.circle(imgFrame, center, radius, (0, 0, 0), 2)
    #
    # print(circles)
    # cv2.imwrite("output/kang"+str(i)+".jpg",imgFrame)
    """
    status – output status vector (of unsigned chars); each element of the vector is set to 1
    if the flow for the corresponding features has been found, otherwise, it is set to 0.
    err – output vector of errors; each element of the vector is set to an error for the
    corresponding feature, type of the error measure can be set in flags parameter;
    if the flow wasn’t found then the error is not defined (use the status parameter to find such cases).
    """
# # count the unique particles appearing in the video with their radii
# def uParticles(i):
#
#     # new frame updation
#     nCircles,newFrame = circleIdentifier(i)
#     nCenters = nCircles[:,:,:2] #center obtained by hough method
#
#     if i==1:
#         circles,oldFrame = circleIdentifier(0)
#         centers=circles[:,:,:2]
#
#     # calculate optical flow
#     updatedCenter, st, err = cv2.calcOpticalFlowPyrLK(oldFrame, newFrame, centers, None, **lk_params)
#     print("nCenters",nCenters)
#     print("updatedCenter",updatedCenter)
#     print(st)
#
#     # TODO: Select good points using st
#     good_new = updatedCenter
#     good_old = centers
#
#     # draw the tracks
#     tFrame=frameGen(i)
#     for k,(new,old) in enumerate(zip(good_new[0], good_old[0])):
#         a,b = new.ravel()
#         c,d = old.ravel()
#         print(k,a,b)
#         tFrame = cv2.circle(tFrame,(a,b),5,color[k].tolist(),-1)
#     cv2.imwrite('tempout/frame'+str(i)+'.jpg',tFrame)
#
#     # Now update the previous frame and previous points
#     # oldFrame = newFrame.copy()
#     centers = updatedCenter
#     oldFrame = newFrame
# #_______________________________________________________________________________
# FUnctions end. start of the program

# capture frames from a camera
cap = cv2.VideoCapture('original.avi')
# get total number of frames
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (30,30),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors for drawing tracks
color = np.random.randint(0,255,(100,3))

# contains center coordinates and radii of the cicles
xCord = []
yCord = []
rad = []

# initialization frame
circles,oldFrame = circleIdentifier(0)
centers=circles[:,:,:2]
print(oldFrame)
for index in range(len(circles[0][0])):
    xCord.append(circles[0][index][0])
    yCord.append(circles[0][index][1])
    rad.append(circles[0][index][2])


# doing the process for each frame
for i in range(1,int(totalFrames)):
	# new frame updation
    nCircles,newFrame = circleIdentifier(i)
    nCenters = nCircles[:,:,:2] #center obtained by hough method

    # calculate optical flow
    updatedCenter, st, err = cv2.calcOpticalFlowPyrLK(oldFrame, newFrame, centers, None, **lk_params)
    print("nCenters",nCenters)
    print("updatedCenter",updatedCenter)
    print(st)

    # TODO: Select good points using st
    good_new = updatedCenter
    good_old = centers

    # draw the tracks
    tFrame=frameGen(i)
    for k,(new,old) in enumerate(zip(good_new[0], good_old[0])):
        a,b = new.ravel()
        c,d = old.ravel()
        print(k,a,b)
        tFrame = cv2.circle(tFrame,(a,b),5,color[k].tolist(),-1)
    cv2.imwrite('tempout/frame'+str(i)+'.jpg',tFrame)

    # Now update the previous frame and previous points
    # oldFrame = newFrame.copy()
    centers = updatedCenter
    oldFrame = newFrame
