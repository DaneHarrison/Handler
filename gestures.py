import math


def leftClick(lmList, mpHands):
    _, thumbTipX, thumbTipY = lmList[mpHands.HandLandmark.THUMB_TIP]
    _, midFingPipX, midFingPipY = lmList[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
    return math.sqrt(
        math.pow(midFingPipX - thumbTipX, 2) + math.pow(midFingPipY - thumbTipY, 2)
    )


def fist(lmList, mpHands):
    return math.sqrt(
        math.pow(index_tip[1] - center[1], 2) + math.pow(index_tip[2] - center[2], 2)
    )
