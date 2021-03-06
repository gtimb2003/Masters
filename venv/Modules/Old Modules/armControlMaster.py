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

# capture init
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Start RealSense pipeline and save depth frames
pipeline = rs.pipeline()
pipeline.start()
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()
rgb = frames.get_color_frame()

# Goto default Birdseye view
arm.set_servo_angle(angle=standBy, speed=50, wait=True)
# Default gripper opening
arm.set_gripper_position(500, wait=True)

# initialization end

while True:
    ################################# QR Detection #############################
    xOut = 0
    yOut = 0

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
    ################################# QR Detection #####################################


    ##################################  ARM CONTROL   ##################################


    arm.set_servo_angle(angle=standBy, speed=50, wait=True)



    xInt = round(remap(yOut, camB, camT, xArmB, xArmT))
    yInt = round(remap(xOut, camR, camL, xArmR, xArmL))

    if xOut:
        arm.set_servo_angle(angle=birdEye, speed=50, wait=True)
        time.sleep(1)

        ################################# Depth Detection ##########################

        xD = int(remap(xOut, 0, 1280, 0, 640))  # remap to match the depth resolution
        yD = int(remap(yOut, 0, 720, 0, 480))

        dist = round(depth.get_distance(xD, yD),2)
        xDR = remap(dist, 0.15, 1, 585.8, 109)  # remap to z axis of robot

        print("distance realsense",dist)
        print("sensor coordinate", xD, yD)
        print("robot z axis", xDR)

        ################################# Depth Detection ##########################

        xInt = round(remap(yOut, camB, camT, xArmB, xArmT))
        yInt = round(remap(xOut, camR, camL, xArmR, xArmL))
        aInt = round(mydegrees)

        print(xInt, yInt)
        # Check if QR is within limit
        if xArmB <= xInt <= xArmT and xArmR <= yInt <= xArmL:
            # Go to position of QR
            # arm.set_servo_angle(angle=[birdEye[0], birdEye[1], birdEye[2], birdEye[3], birdEye[4], birdEye[5], aInt], speed=100, wait=False)

            arm.set_position(xInt, yInt, xDR, 0, 0, 0, speed=100, wait=True)

            # Grab fixture
            arm.set_gripper_position(90, wait=True)

            # return to bird eye position
            arm.set_servo_angle(angle=birdEye, speed=50, wait=True)

            # move to storage location
            arm.set_servo_angle(angle=sLoc, speed=50, wait=True)
            arm.set_gripper_position(500, wait=True)
            arm.set_servo_angle(angle=[-146.4, 3.5, 5, 80, 0, 36, 0], speed=50, wait=True)

            # retract arm
            arm.set_servo_angle(angle=birdEye, speed=50, wait=True)

    else:
        print("No QR")
    ##################################  ARM CONTROL END #################################
