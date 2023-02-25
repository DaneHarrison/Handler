import cv2
import mediapipe as mp
import handTracker

#input image or video
#identify if theres a person
#train model yolo, draws boxes around person

def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        if len(lmList) != 0:
            print(lmList[4])

        cv2.imshow("Video",image)
        cv2.waitKey(1)

    



if __name__ == "__main__":
    main()
