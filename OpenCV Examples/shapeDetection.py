import cv2
import numpy as np

def detectContours(img):
    imgContour = img.copy()

    contours, hierarchy = cv2.findContours(img,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(contours)

        if area > 500: #reduce noise and add drawing
            cv2.drawContours(imgContour, cnt, contourIdx=-1, color=(255, 0, 0), thickness=3)
            peri = cv2.arcLength(curve=cnt,closed=True)
            approxCorners = cv2.approxPolyDP(curve=cnt,epsilon=0.02*peri,closed=True)
            approxNumCorners = len(approxCorners)
            x, y, w, h = cv2.boundingRect(array=approxCorners) #create bounding box

            #Detect Shape
            if approxNumCorners == 3: objectType = "Tri"
            elif approxNumCorners == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05: objectType = "Square"
                else: objectType = "Rectangle"
            elif approxNumCorners > 4: objectType = "Circle"
            else: objectType = "None"

            # draw bounding box and
            cv2.rectangle(imgContour,pt1=(x,y),pt2=(x+w,y+h),color=(0,255,0),thickness=2)
            cv2.putText(imgContour,text=objectType,org=(x+(w//2)-10, y+(h//2)-10),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=0.8,color=(0,0,0),tickness=2)


def detectShapes(imgPath):
    img = cv2.imread(imgPath)

    #Pre process
    img_gray = cv2.cvtColor(img,cv2.COLOR_BG2BGRAY)
    img_blur = cv2.GaussianBlur(img_gray,ksize=(7,7),sigmaX=1)
    img_canny = cv2.Canny(img_blur,threshold1=50,threshold2=50)

    detectContours(img_canny)

    cv2.imshow("Output", img)
    cv2.imshow("Canny Output", img_canny)
    cv2.imshow("Gray Output", img_gray)
    cv2.imshow("Blur Output", img_blur)
    cv2.waitkey(0)