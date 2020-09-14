import cv2

vidcap = cv2.VideoCapture('sampleVideo.mp4')
success,image = vidcap.read()

count = 0
while success:
  cv2.imwrite("Assets/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imshow('image', image)
  cv2.waitKey(100)
  count += 1

cv2.destroyAllWindows()