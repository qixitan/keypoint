# !/usr/bin/python3.8
# -*- coding: UTF-8 -*-
# @Author: qixitan
# @Email: qixitan@qq.com
# @FileName: AIVirtualMouse.py
# @Time: 2022/8/7 11:48

import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy


if __name__ == '__main__':
    detector = htm.handDetector(maxHands=1, detectionCon=0.7, trackCon=0.7)
    ###################################################
    wCam, hCam = 640, 480
    wScr, hScr = autopy.screen.size()  # size of screen
    frameR = 100   # Frame Reduction
    smoothening = 5
    ###################################################
    # print(wScr, hScr)
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0
    while True:
        # 1.Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img, True)
        lmList, _ = detector.findPosition(img)
        # 2.Get the tip of the index and meddle fingers

        if len(lmList) != 0:
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            # 3.Check which are up
            fingers = detector.fingersUp()
            # print(fingers)
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            # 4.Only Index Finger: Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5.Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # 6.Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # 7.Move Mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

                plocX, plocY = clocX, clocY
        # 8.Both Index and middle finger are up: Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9.Find distance between fingers
                length, img, lineInfo = detector.findDistance(p1=8, p2=12, img=img)
                # 10.Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
        # 11. Frame Rate

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # 12. Display

        cv2.imshow("img0", img)
        cv2.waitKey(1)