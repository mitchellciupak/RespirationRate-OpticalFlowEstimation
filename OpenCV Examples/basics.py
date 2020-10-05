import cv2

def openImage(imgPath):
    img = cv2.imread(imgPath)
    cv2.imshow("Output", img)
    cv2.waitkey(0)

def openVideo(vidPath):
    cap = cv2.VideoCapture(vidPath)

    while True:
        isValid, img = cap.read()
        cv2.imshow("Output",img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

def openCamera():
    cap = cv2.VideoCapture(0)

    setIDs = {"horiz": 3, "vert": 4, "brightness": 10}

    # Specify Size
    cap.set(setIDs["horiz"],640)
    cap.set(setIDs["vert"],480)

    # Change brightness (id 10)
    cap.set(setIDs["brightness"],100)