import cv2
import mediapipe as mp
from handTracker import handTracker
from mouseMover import mouseMove, mouseClick

#input image or video
#identify if theres a person
#train model yolo, draws boxes around person

def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        flippedImg = cv2.flip(image, 1)
        image = tracker.handsFinder(flippedImg)
        lmList = tracker.positionFinder(image)
        mpHands = tracker.getHandsModule()
        if len(lmList) != 0:
            print(lmList[mpHands.HandLandmark.INDEX_FINGER_TIP])
            _,xpos,ypos = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
            mouseMove(xpos, ypos)
            
        cv2.imshow("Video",image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
