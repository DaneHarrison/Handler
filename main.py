import cv2
import mediapipe as mp

#input image or video
#identify if theres a person
#train model yolo, draws boxes around person

def main():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils



if __name__ == "__main__":
    main()
