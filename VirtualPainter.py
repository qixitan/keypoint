# -*- coding:utf-8 -*-
# @author:qixitan
# @time:2022/7/24
# @email:qixitan@qq.com

import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm


brushThickness = 15
eraserThickness = 100
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(detectionCon=0.5)
drawColor = (255, 0, 255)

imgCanvas = np.zeros((480, 640, 3), np.uint8)

while True:
    # 1. Import Images
    sueccess, img = cap.read()
    img = cv2.flip(img, 1)
    # print(img.shape)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1)

        # 3. Check Which Finger are Up
        finger = detector.fingersUp()
        # print(finger)

        # 4. If Selection Mode - Two finger are up
        if finger[1] and finger[2]:
            print("Selection Mode")
            # check for click
            if y1 < 120:
                if 120 < x1 < 220:
                    # Choose one
                    print("紫色")
                    drawColor = (255, 0, 255)
                elif 260 < x1 < 360:
                    print("蓝色")
                    drawColor = (255, 0, 0)
                elif 400 < x1 < 500:
                    print("绿色")
                    drawColor = (0, 255, 0)
                elif 540 < x1 < 640:
                    print("黑色")
                    drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if finger[1] and not finger[2]:
            xp, yp = 0, 0
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp ==0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # img[0:120, 0:1200] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("img", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)