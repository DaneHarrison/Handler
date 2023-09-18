from mediapipe import solutions as mp
from abc import ABC, abstractmethod
import math
 
Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class Gesture(ABC):
    def __init__(self):
        self.lastAction = 0

    def calcDist(self, x1, x2, y1, y2):
        dist = None

        if x1 and x2 and y1 and y2:
            dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

        return dist

    @abstractmethod
    def check(self, handTracker):
        pass

    @abstractmethod
    def triggerAction(self, handTracker, mouse):
        pass