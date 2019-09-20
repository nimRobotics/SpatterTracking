import cv2

for k in range(200):
    print("Processing frame ",k)
    img = cv2.imread('frames/OR_'+str(k)+'.png')
    cv2.circle(img,(519,787),170,(0,255,0),1)
    cv2.imwrite("ringGen/RG_"+str(k)+".png",img)
