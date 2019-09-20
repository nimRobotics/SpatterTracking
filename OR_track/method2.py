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
	# number of frames for calculating the average
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

    # drawing the circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for k in circles[0, :]:
            center = (k[0], k[1])
            # circle center
            cv2.circle(imgFrame, center, 1, (0, 100, 100), 2)
            # circle outline
            radius = k[2]
            cv2.circle(imgFrame, center, radius, (0, 0, 0), 2)
    print(str(i)+"th frame")
    print(circles)
    cv2.imwrite("output/OR_"+str(i)+".png",imgFrame)

# count the unique particles appearing in the video with their radii
def uParticles(arg):
    pass

# start of the program

# capture frames from a video
cap = cv2.VideoCapture('original.avi')
# get total number of frames
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# doing the process for each frame
for i in range(int(totalFrames)):
	circleIdentifier(i)
