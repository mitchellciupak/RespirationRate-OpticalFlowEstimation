import cv2 as cv
import numpy as np

# Macros
## Parameters for Harris corner detection  https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
feature_params = dict(maxCorners = 300, qualityLevel = 0.5, minDistance = 2, blockSize = 7)
## Parameters for Lucas-Kanade optical flow https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Pull in video
cap = cv.VideoCapture("SampleVideos/OpticalFlowSampleRR_FastBreaths.mp4")
color = (255, 69, 0) #RGB to draw optical flow track

# Generate first frame and convert to grayscale
isreadValid, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Find the strongest corners (Harris method)
prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)

# Create new frame to draw on
mask = np.zeros_like(first_frame)

while(cap.isOpened()):

    # Generate new frame and convert to grayscale
    isreadValid, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calculates sparse optical flow by Lucas-Kanade method
    next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

    # Selects feature points noted for prev and next
    good_old = prev[status == 1]
    good_new = next[status == 1]

    # Draws the optical flow tracks
    aArr = []
    bArr = []
    for i, (new, old) in enumerate(zip(good_new, good_old)):

        a, b = new.ravel() # Returns a contiguous flattened array as (x, y) coordinates for new point
        aArr.append(a)
        bArr.append(b)

        c, d = old.ravel() # Returns a contiguous flattened array as (x, y) coordinates for old point

        # Draws line between new and old position with green color and 2 thickness
        mask = cv.line(mask, (a, b), (c, d), color, 2)

        # Draws filled circle (thickness of -1) at new position with green color and radius of 3
        frame = cv.circle(frame, (a, b), 3, color, -1)

    # Output Original Frame + optical flow tracks
    output = cv.add(frame, mask)

    # Updates previous frame
    prev_gray = gray.copy()

    # Updates previous good feature points
    prev = good_new.reshape(-1, 1, 2)

    # Opens a new window and displays the output frame
    cv.imshow("sparse optical flow", output)

    #Presses the 'q' key to break
    if cv.waitKey(10) & 0xFF == ord('q'): #10 milliseconds
        break

# Calculate Avg Displacement
def dist(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

avgDistArr = []
for i in range(0,len(aArr) - 1):
    avgDistArr.append(dist(aArr[i],bArr[i],aArr[i+1],bArr[i+1]))

avg = sum(avgDistArr)/len(avgDistArr)
print("Avg Change is", avg, " pixels/frame")

#Todo Fourier Transform to BPM
#print("Breaths Per Min is")

# The following frees up resources and closes all windows
cap.release()
cv.destroyAllWindows()

# Avg Change is 490.2776753874647


#collect all changes
#take sum 
#find mean
