from gestures.gesture import Gesture

from mediapipe import solutions as mp
from datetime import datetime
import win32gui, win32con

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)

 
class Fist(Gesture):
    DELAY = 2 # used to prevent duplicate close window requests

    def check(self, handTracker) -> bool:
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)

        fistDist = self.calcDist(indexTipX, wristX, indexTipY, wristY)

        return fistDist and fistDist < 100

    def triggerAction(self, handTracker, mouse):
        currAction = datetime.now().second

        if currAction - self.lastAction > Fist.DELAY:
            self.lastAction = currAction
            window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
