import cv2

# Opens the Video file
cap= cv2.VideoCapture('IR200f.avi')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('frames/IR_'+str(i)+'.png',frame)
    print("Creating frame "+str(i))
    i+=1

cap.release()
cv2.destroyAllWindows()
