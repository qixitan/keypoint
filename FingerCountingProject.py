# -*- coding:utf-8 -*-
# @author:qixitan
# @time:2022/7/19
# @email:qixitan@qq.com

import cv2
import time
import HandTrackingModule as htm
import os


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    pTime = 0
    detector = htm.handDetector(detectionCon=0.75)
    tipIds = [4, 8, 12, 16, 20]
    while True:
        success, img = cap.read()
        img = detector.findHands(img, True)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            fingers = []
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 2][1]:
                fingers.append((1))
                # print("Index finger open")
            else:
                fingers.append(0)
            # 4 finger
            for i in range(1, 5):
                if lmList[tipIds[i]][2] < lmList[tipIds[i]-2][2]:
                    fingers.append((1))
                    # print("Index finger open")
                else:
                    fingers.append(0)
            # print(fingers)
            totalFingers = fingers.count(1)
            print(totalFingers)

            cv2.rectangle(img, (0, 0), (200, 200), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 150), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"fps:{int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


        cv2.imshow("img", img)
        cv2.waitKey(1)


