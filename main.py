from datetime import datetime
import cv2
import mediapipe as mp
from handTracker import handTracker
from mouseMover import mouseMove,mouseLeftClick,mouseRightClick,detectOS
import math
import win32gui
import win32con

#window properties 
FRAMEWIDTH = 640
FRAMEHEIGHT = 480
MONITORWIDTH = 1920
MONITORHEIGHT = 1080
WINDOWNAME = "Video"

LEFTDEBOUNCETIME = 2
LASTLEFTCLICK = 0
CURRLEFTCLICK = 0

RIGHTDEBOUNCETIME = 2
LASTRIGHTCLICK = 0
CURRRIGHTCLICK = 0

DEBOUNCETIMEFIST = 2
LASTFIST = 0
CURRFIST = 0

MA_WINDOW = 5  # Number of frames to include in moving average
ma_x, ma_y = [], []  # Lists to store cursor positions for moving average

# def scale to monitor size
def scaleToMonitor(xpos, ypos):
    x = xpos * MONITORWIDTH/FRAMEWIDTH
    y = ypos * MONITORHEIGHT/FRAMEHEIGHT
    return x,y

def getSmootherCursorPos(xpos, ypos):
    ma_x.append(xpos)
    ma_y.append(ypos)

    # If moving average lists are longer than window size, remove oldest entry
    if len(ma_x) > MA_WINDOW:
        ma_x.pop(0)
        ma_y.pop(0)

    # Calculate moving average cursor position
    ma_x_avg = sum(ma_x) / len(ma_x)
    ma_y_avg = sum(ma_y) / len(ma_y)

    # return smoothed position
    return ma_x_avg, ma_y_avg

def main():
    #setting up the window properties
    cv2.namedWindow(WINDOWNAME,1)
    cv2.setWindowProperty(WINDOWNAME, cv2.WND_PROP_TOPMOST, 1)
    global LASTCLICK
    global CURRCLICK
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
            #print(lmList[mpHands.HandLandmark.INDEX_FINGER_TIP])
            _,xpos,ypos = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
            scaledX, scaledY = scaleToMonitor(xpos, ypos)
            ma_x_avg, ma_y_avg = getSmootherCursorPos(scaledX, scaledY)

            mouseMove(int(ma_x_avg), int(ma_y_avg))
            # mouseMove(int(scaledX), int(scaledY))

            # Simulate Left Click
            _,thumbTipX,thumbTipY = lmList[mpHands.HandLandmark.THUMB_TIP]
            _,midFingPipX,midFingPipY = lmList[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
            leftClickDist = math.sqrt(math.pow(midFingPipX-thumbTipX, 2) + math.pow(midFingPipY-thumbTipY, 2))
            #print(leftClickDist)
            if leftClickDist < 75:
                CURRLEFTCLICK = datetime.now().second
                #print("left click")
                if CURRLEFTCLICK - LASTLEFTCLICK > LEFTDEBOUNCETIME:
                    LASTLEFTCLICK = CURRLEFTCLICK
                    mouseLeftClick(int(scaledX), int(scaledY))

            # Simulate Right Click
            _,pinkyTipX,pinkyTipY = lmList[mpHands.HandLandmark.PINKY_TIP]
            _,wristX,wristY = lmList[mpHands.HandLandmark.WRIST]
            rightClickDist = math.sqrt(math.pow(pinkyTipX-wristX, 2) + math.pow(pinkyTipY-wristY, 2))
            if rightClickDist > 150:
                CURRRIGHTCLICK = datetime.now().second
                #print("right click")
                if CURRRIGHTCLICK - LASTRIGHTCLICK > RIGHTDEBOUNCETIME:
                    LASTRIGHTCLICK = CURRRIGHTCLICK
                    mouseRightClick(int(scaledX), int(scaledY))
                
            center = lmList[mpHands.HandLandmark.WRIST]
            index_tip = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = lmList[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = lmList[mpHands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = lmList[mpHands.HandLandmark.PINKY_TIP]

            fistDist = (math.sqrt(math.pow(index_tip[1]-center[1], 2) + math.pow(index_tip[2]-center[2], 2)))
            if (100 > fistDist):
                CURRFIST = datetime.now().second
                if CURRFIST - LASTFIST > DEBOUNCETIMEFIST:
                    LASTFIST = CURRFIST
                    #print("fist")
                    hwnd = win32gui.GetForegroundWindow()
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE) 

        cv2.imshow(WINDOWNAME,image)    
            # when hit 'q', terminate the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()

