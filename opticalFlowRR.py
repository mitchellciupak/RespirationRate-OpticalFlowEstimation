#Mitchell Ciupak adapted from https://github.com/ynandwan/OpticalFlowRR
#Imports
from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys, os
import cv2
import numpy as np
import scipy as sp
import sys
from numpy import linalg as LA

#Macros
SIZE = (160, 120)
GRAD_SIZE = (int(160 * 0.25), int(120 * 0.25))
FLOW_MEMORY = 0.85
PFF_MEMORY = 0.85
MA = 10
SIGNAL_MEMORY = 0.80
n = 0

#File I/O
prevGray = None
rrsignal = []
file_name = sys.argv[1]
cap = cv2.VideoCapture(file_name)
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

allrn = []
while (cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        n += 1
        frame = frame.astype(float)
        gray_org = 0.29 * frame[:, :, 2] + 0.59 * frame[:, :, 1] + 0.11 * frame[:, :, 0]
        gray_blur = cv2.GaussianBlur(gray_org, (21, 21), 8, borderType=0)
        gray = cv2.resize(gray_blur, SIZE)
        imx, imy = np.gradient(gray)

        if (n == 1):
            prevGray = gray

        dn = prevGray - gray
        prevGray = gray
        gradNorm2 = np.multiply(imy, imy) + np.multiply(imx, imx)
        gradNorm2[gradNorm2 < 9] = float("inf")
        flowx = np.multiply(imx, dn) / gradNorm2
        flowy = np.multiply(imy, dn) / gradNorm2

        flowx, flowy = cv2.resize(flowx, None, fx=0.25, fy=0.25), cv2.resize(flowy, None, fx=0.25, fy=0.25)
        fn = np.hstack((flowx.flatten(), flowy.flatten()))

        if (n == 1):
            tflow = fn
            dflow = fn
            continue

        tflow = FLOW_MEMORY * tflow + fn
        mag = LA.norm(tflow)

        if (mag > MA):
            tflow = (tflow * MA) / mag

        if (dflow.dot(fn) > 0):
            dflow = PFF_MEMORY * dflow + fn
        else:
            dflow = PFF_MEMORY * dflow - fn

        mag = LA.norm(dflow)
        if (mag > MA):
            dflow = (dflow * MA) / mag
        #
        pffNorm = LA.norm(dflow)
        rn = np.dot(tflow, dflow) / pffNorm
        allrn.append(rn)
        if (len(rrsignal) > 0):
            rrsignal.append(rrsignal[-1] * SIGNAL_MEMORY + rn)
        else:
            rrsignal.append(0)
        #
        if n % 100 == 0:
            print("n: {0}, this rr: {1}".format(n, rn))
        #

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("n: {0}".format(n))
        break

cap.release()
cv2.destroyAllWindows()

plot_rrsignal = np.array(rrsignal)
sigl = len(rrsignal)
plot_rrsignal = plot_rrsignal[int(sigl * 0.06): int(sigl * 0.94)]

fig = plt.figure()
plt.plot(plot_rrsignal[::int(frame_rate / 3)])
plt.show()
fig.savefig('rsignal_' + file_name + '.png')  # Use fig. here

rrate = [0]
hw = 12
for k in range(len(rrsignal[2 * frame_rate:-2 * frame_rate])):
    if (k < hw * frame_rate):
        continue
    # Pdb().set_trace()
    fourier = abs(np.fft.fft(rrsignal[k - hw * frame_rate:k]))
    N = fourier.size
    fourier = fourier[:int(N / 2)]
    freq = np.fft.fftfreq(N, d=1.0 / frame_rate)
    freq = freq[:int(N / 2)]
    m = max(fourier)
    d = [i for i, j in enumerate(fourier) if j == m]
    # Pdb().set_trace()
    rrate.append(60 * freq[d])

fig1 = plt.figure()
plt.plot(rrate)
plt.show()
fig1.savefig('bpm_' + file_name + '.png')  # Use fig. here

avg_rrate = sum(rrate) / len(rrate) * 1.0
print("Average RR rate: %d" % avg_rrate)


#Fast breathing sample
# n: 100, this rr: 3.5251808213334885
# n: 200, this rr: 0.41059284205600627
# n: 300, this rr: 2.078626586391098
# n: 400, this rr: -0.22163602410905672
# n: 500, this rr: 5.0181485621144555
# n: 600, this rr: 3.6952834443784894
# n: 700, this rr: 5.81976098438961
# n: 800, this rr: -3.1580700624345694
# n: 900, this rr: 2.790759134305223
