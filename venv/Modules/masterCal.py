# Imports
import os
import sys
import time
import math
import pandas as pd
import numpy as np
import csv
import cv2
from pyzbar.pyzbar import decode
import pyrealsense2 as rs

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from xarm.wrapper import XArmAPI
from configparser import ConfigParser

# Connect to xArm
parser = ConfigParser()
parser.read('C:\\Users\\geo_t\\PycharmProjects\\xArm\\xarm\\wrapper\\robot.conf')
ip = parser.get('xArm', 'ip')

# xArm init
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# Gripper init
arm.set_gripper_mode(0)
arm.set_gripper_enable(True)
arm.set_gripper_speed(5000)

# Interpolation function
def remap(x, oMin, oMax, nMin, nMax):
    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x - oldMin) * (newMax - newMin) / (oldMax - oldMin)
    if reverseInput:
        portion = (oldMax - x) * (newMax - newMin) / (oldMax - oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result

# Variables
birdEye = [0, 3.3, 0, 116, 0, 112, 0]  # Default Birdseye view



# robo position INIT
# Default gripper opening
arm.set_gripper_position(500, wait=True)

# capture from Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

arm.set_servo_angle(angle=birdEye, speed=50, wait=True)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        poly = barcode.polygon  # .polygon creates an array with coordinates of each corner of the qr code
        # Take the 2 bottom corners
        xy2 = poly[2]
        x2 = int(xy2[0])
        y2 = int(xy2[1])

        xy3 = poly[3]
        x3 = int(xy3[0])
        y3 = int(xy3[1])

        # get angle of bottom
        myradians = math.atan2(y2 - y3, x2 - x3)
        mydegrees = round(math.degrees(myradians))

        # calculate the midpoint between the two bottom points
        xOut = int((x3 + x2) / 2)
        yOut = int((y3 + y2) / 2)

        print(xOut, yOut)
    cv2.namedWindow('feed', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('feed', img)
    cv2.waitKey(1)