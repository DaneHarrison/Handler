from gestures.gesture import Gesture

from mediapipe import solutions as mp
import random #########################3
Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class Setup(Gesture):
    def __init__(self, inSetUp):
        self.inSetUp = inSetUp


    def check(self, handTracker) -> bool:
        return self.inSetUp

    def triggerAction(self, handTracker, mouse):
        # tip of thumb should be far from index
        thumbX, thumbY = handTracker.readPointPosi(Points.THUMB_TIP)
        indexMcpX, indexMcpY = handTracker.readPointPosi(Points.INDEX_FINGER_MCP)

        # other fingers should be bent
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        middleX, middleY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)
        ringX, ringY = handTracker.readPointPosi(Points.RING_FINGER_TIP)
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)
        
        # Pinky should stick out
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)

        thumbToIndex = self.calcDist(thumbX, indexMcpX, thumbY, indexMcpY)
        wristToIndex = self.calcDist(wristX, indexTipX, wristY, indexTipY)
        wristToMiddle = self.calcDist(wristX, middleX, wristY, middleY)    
        wristToRing = self.calcDist(wristX, ringX, wristY, ringY)
        wristToPinky = self.calcDist(wristX, pinkyX, wristY, pinkyY)
        
        thumbToIndex = self.normalize(thumbToIndex, handTracker)
        wristToIndex = self.normalize(wristToIndex, handTracker)
        wristToMiddle = self.normalize(wristToMiddle, handTracker)
        wristToRing = self.normalize(wristToRing, handTracker)
        wristToPinky = self.normalize(wristToPinky, handTracker)

        indexDipX, indexDipY = handTracker.readPointPosi(Points.INDEX_FINGER_DIP)
        currLength = self.calcDist(indexDipX, indexTipX, indexDipY, indexTipY)

        showing = False
        if thumbToIndex and wristToIndex and wristToMiddle and wristToRing and wristToPinky:
            # if currLength >= 38 and currLength <= 45:
            #    print(f'thumbToIndex: {thumbToIndex}, wristToIndex: {wristToIndex}, wristToMiddle: {wristToMiddle}, wristToRing: {wristToRing}, wristToPinky: {wristToPinky}') 
        
        #160.64629495931476, wristToIndex: 223.49092146877285, wristToMiddle: 215.1011565771213, wristToRing: 208.20765439922556, wristToPinky: 357.2412375
            if thumbToIndex >= 150 and wristToIndex <= 225 and wristToMiddle <= 220 and wristToRing <= 215 and wristToPinky >= 355:
                #print(f'thumbToIndex: {thumbToIndex}, wristToPinky: {wristToPinky}, wristToIndex: {wristToIndex}, wristToMiddle: {wristToMiddle}, wristToRing: {wristToRing}') 
            # if thumbToMiddle <= 60 and wristToIndex >= 300 and wristToRing >= 300 and wristToPinky >= 250:
                print(random.randbytes(5))



        # if thumbToIndex and wristToMiddle and wristToRing and wristToPinky:
        #     #print(f'thumbToIndex: {thumbToIndex}')
        #     if thumbToIndex >= 130 and wristToMiddle <= 110 and wristToRing <= 90 and wristToPinky <= 120:

        #             print(random.randbytes(5))
