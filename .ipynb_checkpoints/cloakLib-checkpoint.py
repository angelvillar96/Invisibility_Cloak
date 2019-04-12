import numpy as np
import scipy as sp
import os, time, sys, cv2
from matplotlib import pyplot as plt



#Creating a video capture object
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

#asking user to start
start=""
while(start!="s" and start!="s"):
    start = input("Press S to obtain initial image!")
time.sleep(5)

#capturing the image (the loop improves quality)
background=0
for i in range(30):
    ret,background = cap.read()
print("Initial Frame Captured")
    
plt.figure()
plt.imshow(background[:,:,::-1])
plt.title("Static Background")
plt.show()
    
#flipping the image
background = np.flip(background ,axis=1)

#asking user to start
key=""
while(key!="s" and key!="s"):
    key = input("Press S to start!")


#iterating so we make a video
while(cap.isOpened()):

    #obtaining image
    ret, img = cap.read()

    #flipping and converting to HSV space
    img = np.flip(img,axis=1)
    hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #using a mask for the desired color
    lowerBound = np.array([15,5,5])
    upperBound = np.array([60,255,255])
    mask = cv2.inRange( hsvImage , lowerBound , upperBound)

    #deleting really small regions
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((32,32),np.uint8))

    #getting an image with just the cloak
    cloakImage = np.zeros( (background.shape) )
    cloakImage[mask==255,:] = background[mask==255,::-1]/255

    #getting the invisible-cloak image
    img[np.where(mask==255)] = background[np.where(mask==255)]

    #cv2.imshow("Magic!!",cloakImage)
    cv2.imshow('Magic!!',img)
    out.write(img)
    
    k = cv2.waitKey(10)
    if k == 27:
        break