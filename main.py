import cv2
import mediapipe as mp
from handTracker import handTracker
from mouseMover import mouseMove, mouseClick
import math

#input image or video
#identify if theres a person
#train model yolo, draws boxes around person
    
FRAMEWIDTH = 640
FRAMEHEIGHT = 480
# def scale



def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAMEWIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAMEHEIGHT)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        flippedImg = cv2.flip(image, 1)
        image = tracker.handsFinder(flippedImg)
        lmList = tracker.positionFinder(image)
        mpHands = tracker.getHandsModule()
        if len(lmList) != 0:
            #track the tip of the index finger to move the mouse
            _,xpos,ypos = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
            mouseMove(xpos, ypos)

            # Find the distance to determine if a left click action should be done
            _,x1,y1 = lmList[mpHands.HandLandmark.THUMB_TIP]
            _,x2,y2 = lmList[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
            distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
            #print(distance)
            if distance < 75:
                print("click")
            
        cv2.imshow("Video",image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()

