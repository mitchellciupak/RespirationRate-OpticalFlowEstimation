import cv2

vid = cv2.VideoCapture(0)

while True:
    check,frame = vid.read()
    print(check)
    print(frame)
    cv2.imshow("Caps", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

vid.release()