from gestures.gesture import Gesture

from mediapipe import solutions as mp

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)

 
class Setup(Gesture):
    def __init__(self, inSetUp):
        self.inSetUp = inSetUp

    def check(self, handTracker) -> bool:
        return self.inSetUp

    def triggerAction(self, handTracker, mouse):
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        print(self.calcDist)
