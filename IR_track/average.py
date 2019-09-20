import cv2
import numpy as np

# modify the data type
# setting to 32-bit floating point
img = cv2.imread("thresh/TH_0.png")
averageValue1 = np.float32(img)

# loop runs if capturing has been initialized.
for i in range(10):
	img = cv2.imread("thresh/TH_"+str(i)+".png")

	# using the cv2.accumulateWeighted() function
	# that updates the running average
	cv2.accumulateWeighted(img, averageValue1, 0.002)

	# converting the matrix elements to absolute values
	# and converting the result to 8-bit.
	resultingFrames1 = cv2.convertScaleAbs(averageValue1)

	# the window showing output of alpha value 0.02
cv2.imwrite('averageValue1.jpg', resultingFrames1)
