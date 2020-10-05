import cv2
import numpy as np

def createBlueImg():
    width = 512
    height = 512
    numChannels = 3
    img = np.zeros((width,height,numChannels),np.uint8)
    img[:] = 255,0,0 #blue
    cv2.imshow("Output",img)
    cv2.waitkey(0)

def createGreenLine():
    width = 512
    height = 512
    numChannels = 3
    img = np.zeros((width, height, numChannels), np.uint8)
    cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),2) #From 0,0 to 512,512 w/ thickness=2
    cv2.imshow("Output", img)
    cv2.waitkey(0)

def createRedRectange():
    width = 512
    height = 512
    numChannels = 3
    img = np.zeros((width, height, numChannels), np.uint8)
    cv2.line(img,(0,0),(250,350),(0,0,255),cv2.FILLED) #From 0,0 to 250,350 w/ filling
    cv2.imshow("Output", img)
    cv2.waitkey(0)

def createRedCircle():
    width = 512
    height = 512
    numChannels = 3
    img = np.zeros((width, height, numChannels), np.uint8)
    cv2.circle(img,(256,256),50,(0,0,255),2)
    cv2.imshow("Output", img)
    cv2.waitkey(0)

def addText2Img():
    width = 512
    height = 512
    numChannels = 3
    img = np.zeros((width, height, numChannels), np.uint8)

    cv2.putText(img,"HELLO WORLD",(300,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3) #scale = 1
    cv2.imshow("Output", img)
    cv2.waitkey(0)