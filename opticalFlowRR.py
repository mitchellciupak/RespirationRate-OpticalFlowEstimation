# Estimated Respiration Rate from Lucas-Kanade Optical Flow

import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
    USAGE: optical_flow.py [<video_source>]
    NOTES: defaults to cam
'''

MAX_CORNERS = 200

if __name__ == '__main__':
    import sys

    # Import Video
    try:
        fptr = sys.argv[1]
    except:
        fptr = 0

    cap = cv2.VideoCapture(fptr)
    fps = cap.get(cv2.CAP_PROP_FPS)
    isValid, firstFrame = cap.read()

    if not isValid:
        quit(0)

    # [Detect Corners of First Frame](https://docs.opencv.org/master/d4/d8c/tutorial_py_shi_tomasi.html)
    ff_gray = cv2.cvtColor(firstFrame,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(ff_gray,mask=None,maxCorners=MAX_CORNERS,qualityLevel=0.005,minDistance=10,blockSize=7)
    #corners = np.int0(corners)

    # Init Vars
    prevImg_gray = ff_gray.copy()
    prevFrame = firstFrame.copy()
    mask = np.zeros_like(firstFrame)
    frameCount = 1
    x = []
    y = []
    # Measure Change in corners over time
    while cap.isOpened():
        isValid, nextFrame = cap.read()
        if not isValid:
            break

        frameCount += 1
        nextImg_gray = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)

        # Calculates sparse optical flow, Lucas-Kanade
        LKargs = dict(winSize=(15, 15), maxLevel=2,criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        nextP, status, error = cv2.calcOpticalFlowPyrLK(prevImg_gray, nextImg_gray, corners, None, **LKargs)

        # Draw Tracks (for all 1 points)
        for i, (new, old) in enumerate(zip(nextP[status == 1],corners[status == 1])):
            nextx, nexty = new.ravel()
            prevx, prevy = old.ravel()

            # Update x and y for measurements
            x.append(nextx)
            y.append(nexty)

            # Create line on mask from prev pos to next pos (green)
            mask = cv2.line(mask,pt1=(nextx,nexty),pt2=(prevx,prevy),color=(255,69,0),thickness=2)

            # Create filled circle at next pos (green)
            processedImg = cv2.circle(nextFrame,center=(nextx,nexty),radius=3,color=(255,69,0),thickness=-1)


        # Update nf to prev
        prevImg_gray = nextImg_gray.copy()
        corners = nextP[status == 1].reshape(-1, 1, 2)

        # Output Frame + Mask
        output = cv2.add(processedImg, mask)
        cv2.imshow("Sparse Optical Flow", output)

        # Presses the 'q' key to break
        if cv2.waitKey(10) & 0xFF == ord('q'):  # 10 milliseconds
            break

    cap.release()
    cv2.destroyAllWindows()


"""DATA PROCESSING"""

# Create Avg Displacement Array
dispPerFrame = []
for i in range(0,int(len(x)/MAX_CORNERS)):
    disp = []

    for j in range(0,MAX_CORNERS-1):
        disp.append(((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2)**0.5)

    dispPerFrame.append(sum(disp))

# Plot Displacement vs Frame
plt.plot(range(0,len(dispPerFrame)), dispPerFrame)
plt.xlabel('Frame')  # Add an x-label to the axes.
plt.ylabel('Displacement (pixels)')  # Add a y-label to the axes.
plt.title("Displacement vs Frame")
plt.show()

#Create Displacement per Second Array
dispPerSecond = []
prev = 0
for i in range(1,len(dispPerFrame)):
    if i%int(fps) == 0:
        dispPerSecond.append(sum(dispPerFrame[prev:i]))
        prev = i

# Plot Displacement vs. Time
plt.plot(range(0, len(dispPerSecond)), dispPerSecond)
plt.xlabel('Time (sec)')  # Add an x-label to the axes.
plt.ylabel('Displacement (pixels)')  # Add a y-label to the axes.
plt.title("Displacement vs Time")
plt.show()



def get_inflection_points(arr, n=1):
    """
    returns inflextion points from array
        arr: array
        n: n-th discrete difference
    """
    inflections = []
    dx = 0
    for i, x in enumerate(np.diff(arr, n)):
        if x >= dx and i > 0:
            inflections.append(i*n)
        dx = x
    return inflections

golden = (1 + 5 ** 0.5) / 2
inflectionCount = len(get_inflection_points(dispPerSecond)) / golden
print("Estimated Breaths in Cap: ",inflectionCount)
print("Estimated BPM: ",inflectionCount/len(dispPerSecond))
