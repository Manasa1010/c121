import time
import cv2
import numpy as np

#save the output in a file
fourcc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter("manasa_magic.avi",fourcc,20.0,(640,480))

#starting the web cam and allowing it to start by making the code sleep for 2 sec

cap=cv2.VideoCapture(0)
time.sleep(2)
bg=0

for i in range(60):
    ret,bg=cap.read()
#flipping the background to get rid of the mirroring effect
bg=np.flip(bg,axis=1)

#reading the captured frame until the cam is open
while(cap.isOpened()):
    ret,img=cap.read()
    if not ret:
        break
    img=np.flip(img,axis=1)

    #converting the color from bgr to hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #creating the mask to detect red color(color can be changed by changing the value)
    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)

    mask1=mask1+mask2

    #opening and expanding the image where there is mask 1
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    #selecting the part which does not have red
    mask2=cv2.bitwise_not(mask1)

    #part of image without red color
    res1=cv2.bitwise_and(img,img,mask=mask2)
    #part of image with red color
    res2=cv2.bitwise_and(bg,bg,mask=mask1)

    final_output=cv2.addWeighted(res1,1,res2,1,0)
    output_file.write(final_output)
    cv2.imshow("magic",final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
