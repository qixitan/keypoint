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
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        success, img = cap.read()
        cv2.imshow("img0", img)
        cv2.waitKey(1)