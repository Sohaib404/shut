import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, frame, draw=True):
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(frameRGB)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
                
        return frame
    
    def findPosition(self, frame, handNo=0, draw=True):

        lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        return lmList
                





def main():

    cap = cv.VideoCapture(0)
    detector = handDetector()
    pTime = 0
    cTime = 0

    while True:
        success, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
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

if __name__ == "__main__":
    main()