from gestures.gesture import Gesture 

from mediapipe import solutions as mp
from datetime import datetime

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
 
 
class ThumbIn(Gesture):
    LEFTDEBOUNCETIME = 2 # Used to prevent duplicate left click requests


    def check(self, handTracker):
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        pinkyTipX, pinkyTipY = handTracker.readPointPosi(Points.PINKY_TIP)
        midFingTipX, midFingTipY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)

        ssDist1 = self.calcDist(midFingTipX, wristX, midFingTipY, wristY)
        ssDist2 = self.calcDist(pinkyTipX, midFingTipX, pinkyTipY, midFingTipX)
        
        return ssDist1 and ssDist1 > 50 and ssDist2 and ssDist2 < 75

    def triggerAction(self, handTracker, mouse):
        currAction = datetime.now().second
        x, y = handTracker.readPointPosi()

        if currAction - self.lastAction > ThumbIn.RIGHTDEBOUNCETIME:
            self.lastAction = currAction
            mouse.leftClick(int(x), int(y))
