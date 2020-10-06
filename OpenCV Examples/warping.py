import cv2

def warpProspectiveImg(imgPath):
    #Takes in a set of cards from a slanted angle and returns one of the cards top down

    img = cv2.imread(imgPath)

    #Define all points of imgase slection
    width, height = 250,350
    pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOut = cv2.warpPerspective(img,matrix,(width,height))
    cv2.imshow("Warped Output", imgOut)
    cv2.waitkey(0)


def combineImages(imgPath1,imgPath2):

    # Stack image next to eachother
    ## Need to share number of channels
    img = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2)
    imgHor = np.hstack((img,img2))
    cv2.imshow("Horiz Output", imgHor)

    # Stack images ontop of eachother
    imgVert = np.vstack((img, img2))
    cv2.imshow("Vert Output", imgVert)

    cv2.waitkey(0)

def smartCombineImages(imgPath1,imgPath2):

    img = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2)

    scale = 0.5
    imgStack = stackImages(scale,([img,img2],[img2,img])) #must have same number of cols and rows

    cv2.imshow("Vert Output", imgStack)
    cv2.waitkey(0)
