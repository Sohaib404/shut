import cv2 as cv
import mediapipe as mp
import time
import HandTrackingModule as htm


cap = cv.VideoCapture(0)
detector = htm.handDetector()
pTime = 0
cTime = 0

while True:
    success, frame = cap.read()
    frame = detector.findHands(frame, draw=False)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        print(lmList[8])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX, 3, (0,0,225), 3)

    cv.imshow("Frame", frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()