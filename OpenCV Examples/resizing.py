import cv2

'''
Images are a 2D array (x,y) that starts in the top left of the image
    Meaning that +x is right and +y is south
'''

def resizeImg(imgPath,newWidth,newHeight):
    '''unit of measure: pixel'''
    img = cv2.imread(imgPath)
    height, width, numChannels = img.shape

    imgResize = cv2.resize(img,(newWidth,newHeight))

    cv2.imshow("Resized Output", imgResize)
    print("Change in height is:",height - newHeight, ". Change in width is:",width - newWidth)
    cv2.waitkey(0)

def cropImg(imgPath,newWidth,newHeight):
    '''unit of measure: pixel'''
    img = cv2.imread(imgPath)
    height, width, numChannels = img.shape

    imgCropped = img[0:newWidth,newWidth:newHeight]

    cv2.imshow("Cropped Output", imgCropped)
    cv2.waitkey(0)

