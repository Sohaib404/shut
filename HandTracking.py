import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, frame = cap.read()
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    result = hands.process(frameRGB)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 8 or id == 4:
                    cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX, 3, (0,0,225), 3)

    cv.imshow("Frame", frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()