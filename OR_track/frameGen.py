import cv2

# Opens the Video file
cap= cv2.VideoCapture('original.avi')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('frames/IR_'+str(i)+'.png',frame)
    print("Creating frame "+str(i))
    i+=1
    if i==200:
        break

cap.release()
cv2.destroyAllWindows()
