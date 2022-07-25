# -*- coding:utf-8 -*-
# @author:qixitan
# @time:2022/7/24
# @email:qixitan@qq.com

import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)

while True:
    # 1. Import Images
    sueccess, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1)

        # 3. Check Which Finger are Up
        finger = detector.fingersUp()
        print(finger)

        # 4. If Selection Mode - Two finger are up

        # 5. If Drawing Mode - Index finger is up




    cv2.imshow("img", img)
    cv2.waitKey(1)