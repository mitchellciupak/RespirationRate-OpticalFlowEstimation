import cv2
import numpy as np

def cannyDetection(imgPath):
    img = cv2.imread(imgPath)
    imgCanny = cv2.Canny(img,100,100)
    cv2.imshow("Canny Output", imgCanny)
    cv2.waitkey(0)

def dialateImg(imgPath):
    # Increase edge thickness
    img = cv2.imread(imgPath)
    imgCanny = cv2.Canny(img, 100, 100)

    kernal = np.ones((5, 5), np.uint8)
    imgDialation = cv2.dilate(imgCanny,kernal,iterations=1)

    cv2.imshow("Dilated Output", imgDialation)
    cv2.waitkey(0)


def erodeImg(imgPath):
    # Decrease edge thickness
    img = cv2.imread(imgPath)
    imgCanny = cv2.Canny(img, 100, 100)

    kernal = np.ones((5, 5), np.uint8)
    imgDialation = cv2.dilate(imgCanny, kernal, iterations=1)
    imgEroded = cv2.erode(imgDialation,kernal,iterations=1)

    cv2.imshow("Eroded Output", imgEroded)
    cv2.waitkey(0)