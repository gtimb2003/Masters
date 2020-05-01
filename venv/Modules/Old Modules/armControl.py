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
from pyzbar.pyzbar import decode
import pyrealsense2 as rs

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from xarm.wrapper import XArmAPI
from configparser import ConfigParser

# Connect to xArm
parser = ConfigParser()
parser.read('C:\\Users\\geo_t\\PycharmProjects\\xArm\\xarm\\wrapper\\robot.conf')
ip = parser.get('xArm', 'ip')


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

# xArm init
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# Gripper init
arm.set_gripper_mode(0)
arm.set_gripper_enable(True)
arm.set_gripper_speed(5000)

# Variables
birdEye = [0, 3.3, 0, 116, 0, 112, 0]  # Default Birdseye view
sLoc = [-146.4, 3.5, 5, 40, 0, 36, 0]
standBy = [0, -65, 0, 69, 0, 113.4, 0]
# camera area calibration DLT
camR = 1143
camL = 237
camB = 509
camT = 99
# xArm reach calibration
xArmB = 277.7
xArmT = 619.2
xArmR = -402.1
xArmL = 284.7
# Paths
filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
filepathY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
filepathA = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\angle.txt"

# Goto default Birdseye view
arm.set_servo_angle(angle=standBy, speed=50, wait=True)
# Default gripper opening
arm.set_gripper_position(500, wait=True)

while True:
    arm.set_servo_angle(angle=standBy, speed=50, wait=True)
    # Read the files for the location of the QR Code
    xFile = open(filepathX, "r+")
    yFile = open(filepathY, "r+")

    # In case of an out of range situation, multiple reads of the file can crash the code that is why I put this delay

    # inverted x and y because camera and robot has different point of reference
    # read value from file, interpolate it and store it
    yPre = int(yFile.read())
    xPre = int(xFile.read())

    xInt = round(remap(yPre, camB, camT, xArmB, xArmT))
    yInt = round(remap(xPre, camR, camL, xArmR, xArmL))

    # close the file for stability
    xFile.close()
    yFile.close()

    if xPre:
        arm.set_servo_angle(angle=birdEye, speed=50, wait=True)
        time.sleep(2)
        # Read the files for the location of the QR Code
        xFile = open(filepathX, "r+")
        yFile = open(filepathY, "r+")
        aFile = open(filepathA, "r+")

        # In case of an out of range situation, multiple reads of the file can crash the code that is why I put this delay
        time.sleep(1)

        # inverted x and y because camera and robot has different point of reference
        # read value from file, interpolate it and store it
        yPre = int(yFile.read())
        xPre = int(xFile.read())
        angle = int(aFile.read())  # read angle

        xInt = round(remap(yPre, camB, camT, xArmB, xArmT))
        yInt = round(remap(xPre, camR, camL, xArmR, xArmL))
        aInt = round(angle)

        # close the file for stability
        xFile.close()
        yFile.close()
        aFile.close()

        print(xInt, yInt)
        # Check if QR is within limit
        if xArmB <= xInt <= xArmT and xArmR <= yInt <= xArmL:
            time.sleep(1)
            # Go to position of QR
            arm.set_position(xInt, yInt, 140, 0, 0, 0, speed=100, wait=True)
            # Grab fixture
            arm.set_gripper_position(90, wait=True)

            # return to bird eye position
            arm.set_servo_angle(angle=birdEye, speed=50, wait=True)

            # move to storage location
            arm.set_servo_angle(angle=sLoc, speed=50, wait=True)
            arm.set_gripper_position(500, wait=True)
            arm.set_servo_angle(angle=[-146.4, 3.5, 5, 80, 0, 36, 0], speed=50, wait=True)

            # arm.set_position(5, 599, 500, 180, 0, 87, speed=60, wait=True)

            # retract arm
            # arm.set_servo_angle(angle=[-59, -27, 117, 124, 34, 173, -13], speed=50, wait=True)
            arm.set_servo_angle(angle=birdEye, speed=50, wait=True)

    else:
        print("No QR")
