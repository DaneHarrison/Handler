from gestures.gesture import Gesture

from mediapipe import solutions as mp
from datetime import datetime

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class PinkyIn(Gesture):
    RIGHTDEBOUNCETIME = 2 # used to prevent duplicate right click requests


    def check(self, handTracker) -> bool:
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        pinkyTipX, pinkyTipY = handTracker.readPointPosi(Points.PINKY_TIP)

        rightClickDist = self.calcDist(pinkyTipX, wristX, pinkyTipY, wristY)

        return rightClickDist and rightClickDist > 150

    def triggerAction(self, handTracker, mouse):
        currAction = datetime.now().second
        x, y = handTracker.readPointPosi()

        if currAction - self.lastAction > PinkyIn.RIGHTDEBOUNCETIME:
            self.lastAction = currAction
            mouse.rightClick(int(x), int(y))
