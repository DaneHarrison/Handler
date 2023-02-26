from datetime import datetime
import cv2
import mediapipe as mp
from handTracker import handTracker
from mouseMover import mouseMove,mouseLeftClick,mouseRightClick,detectOS
import math
import win32gui
import win32con
from gestures import leftClick, fist
import win32api

#window properties 
FRAMEWIDTH = 640
FRAMEHEIGHT = 480
MONITORWIDTH = 1920
MONITORHEIGHT = 1080
WINDOWNAME = "Hackethon 2023 group 15"

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

def smoothMouseMove(lmList, mpHands):
    _,xpos,ypos = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
    scaledX, scaledY = scaleToMonitor(xpos, ypos)
    ma_x_avg, ma_y_avg = getSmootherCursorPos(scaledX, scaledY)
    mouseMove(int(ma_x_avg), int(ma_y_avg))
    return scaledX, scaledY

def calcDist( x1, x2, y1, y2):
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

def handleLeftClick(x, y):
    global LASTLEFTCLICK
    global CURRLEFTCLICK
    CURRLEFTCLICK = datetime.now().second
    #print("left click")
    if CURRLEFTCLICK - LASTLEFTCLICK > LEFTDEBOUNCETIME:
        LASTLEFTCLICK = CURRLEFTCLICK
        mouseLeftClick(int(x), int(y))

def handleRightClick(x, y):
    global LASTRIGHTCLICK
    global CURRRIGHTCLICK
    CURRRIGHTCLICK = datetime.now().second
    #print("right click")
    if CURRRIGHTCLICK - LASTRIGHTCLICK > RIGHTDEBOUNCETIME:
        LASTRIGHTCLICK = CURRRIGHTCLICK
        mouseRightClick(int(x), int(y))

def handleFist():
    global LASTFIST
    global CURRFIST
    CURRFIST = datetime.now().second
    if CURRFIST - LASTFIST > DEBOUNCETIMEFIST:
        LASTFIST = CURRFIST
        #print("fist")
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE) 

def main():
    global LASTLEFTCLICK
    global CURRLEFTCLICK
    global LASTRIGHTCLICK
    global CURRRIGHTCLICK
    global LASTFIST
    global CURRFIST

    #setting up the window properties
    cv2.namedWindow(WINDOWNAME,1)
    cv2.setWindowProperty(WINDOWNAME, cv2.WND_PROP_TOPMOST, 1)
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
            scaledX, scaledY =smoothMouseMove(lmList, mpHands)

            # Finger Coordinates
            _, thumbTipX, thumbTipY = lmList[mpHands.HandLandmark.THUMB_TIP]
            _, midFingPipX, midFingPipY = lmList[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
            _, pinkyTipX, pinkyTipY = lmList[mpHands.HandLandmark.PINKY_TIP]
            _, wristX, wristY = lmList[mpHands.HandLandmark.WRIST]
            _, indexTipX, indexTipY = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
            _, midFingTipX, midFingTipY = lmList[mpHands.HandLandmark.MIDDLE_FINGER_TIP]

            leftClickDist = calcDist(midFingPipX, thumbTipX, midFingPipY, thumbTipY) 
            leftClickDist2 = calcDist(midFingTipX, wristX, midFingTipY, wristY)
            #print(leftClickDist)
            if leftClickDist < 75 and leftClickDist2 < 75:
                handleLeftClick(scaledX, scaledY)

            # Simulate Right Click
            
            rightClickDist = calcDist(pinkyTipX, wristX, pinkyTipY, wristY)
            if rightClickDist > 150:
                handleRightClick(scaledX, scaledY)
                
            # Simulate Fist (Minimize Current Window)
            fistDist = calcDist(indexTipX, wristX, indexTipY, wristY)
            if (100 > fistDist):
                handleFist()
                
        cv2.imshow(WINDOWNAME,image)    
            # when hit 'q', terminate the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()

