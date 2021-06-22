import cv2 as cv
import time
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.75)
pTime = 0
cTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(frame, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(frame, (x2, y2), 15, (255, 0, 255), cv.FILLED)
        cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        # Hand range 20 - 240
        # Volume Range -50 to 0

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX, 3, (0,0,225), 3)

    cv.imshow("Frame", frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()