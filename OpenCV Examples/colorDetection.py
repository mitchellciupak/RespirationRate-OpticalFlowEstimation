import cv2
import numpy as np

def empty(arg):
    pass

def colorDetection(imgPath):

    # Define color limits to identify with adjustable track bar
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    while True:
        img = cv2.imread(imgPath)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hue_min = cv2.getTrackbarPos("Hue Min","TrackBars")
        hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        val_max = cv2.getTrackbarPos("Val Max", "TrackBars")

        #Color
        lower = np.array([hue_min,sat_min,val_min])
        upper = np.array([hue_max,sat_max,val_max])
        mask = cv2.inRange(imgHSV,lower,upper) #color that you want as white and everything else as white
        imgResults = cv2.bitwise_and(img,img,mask=mask)

        cv2.imshow("Orig Output", img)
        cv2.imshow("HSV Output", imgHSV)
        cv2.imshow("Mask Output", mask)
        cv2.imshow("Results", imgResults)
        cv2.waitkey(1)