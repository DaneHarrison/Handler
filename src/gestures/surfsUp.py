from gestures.gesture import Gesture

from mediapipe import solutions as mp
from datetime import datetime
import numpy as np
import os, cv2, pyautogui

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class SurfsUp(Gesture):
    DEBOUNCETIMESS = 5 # Used to prevent duplicate screen shot requests


    def check(self, handTracker):
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        pinkyTipX, pinkyTipY = handTracker.readPointPosi(Points.PINKY_TIP)
        midFingTipX, midFingTipY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)

        ssDist1 = self.calcDist(midFingTipX, wristX, midFingTipY, wristY)
        ssDist2 = self.calcDist(pinkyTipX, midFingTipX, pinkyTipY, midFingTipX)
        
        return ssDist1 and ssDist1 > 100 and ssDist2 and ssDist2 > 200

    def triggerAction(self, handTracker, mouse):
        currAction = datetime.now().second
        cwd = os.getcwd()
        os.chdir(cwd)

        if currAction - self.lastAction > SurfsUp.DEBOUNCETIMESS:
            self.lastAction = currAction

            img = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            cv2.imwrite("screenshot.png", img)