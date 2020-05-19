# Imports
import os
import sys
import time
import math
import numpy as np
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
birdEye = [0.0, 3.3000077168354895, 0.0, 116.00000387815524, 4.119222772313541, 113.93036573058367,
           0.0]  # Default Birdseye view
# birdEye =[429.121399, 8.58317, 661.836731, -3.075262, 0.020507, 0.029147]#birdeye position
sLoc = [-65.2, 27.9, 0, 56.1, -0.2, 27.8, -65]
sLocRes = [0, 7, 0, 107, 0, 100, 0]
standBy = [0, -65, 0, 69, 0, 113.4, 0]
# camera area calibration DLT
camL = 390
camR = 1127
camLR = [camL, camR]
camT = 14
camB = 319
camTB = [camT, camB]

# xArm reach calibration
xArmL = 240
xArmR = -303
xArmLR = [xArmL, xArmR]
xArmT = 591
xArmB = 361
xArmTB = [xArmT, xArmB]

# speed of joints
speed = 50

# robo position INIT
# Goto default Birdseye view
arm.set_servo_angle(angle=standBy, speed=speed, wait=True)
# Default gripper opening
arm.set_gripper_position(800, wait=True)

# capture from Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()

    arm.set_servo_angle(angle=standBy, speed=speed, wait=True)
    arm.set_state(state=0)
    for barcode in decode(img):
        arm.set_servo_angle(angle=birdEye, speed=speed, wait=True)
        arm.set_state(state=0)
        time.sleep(2)
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
        xPos = int((x3 + x2) / 2)
        yPos = int((y3 + y2) / 2)
        xLoc = round(remap(yPos, camB, camT, xArmB, xArmT))
        yLoc = round(remap(xPos, camR, camL, xArmR, xArmL))
        print(xLoc, yLoc)
        print(mydegrees)

        if xArmB <= xLoc <= xArmT and xArmR <= yLoc <= xArmL:
            # Go to position of QR
            arm.set_servo_angle(angle=sLocRes, speed=speed, wait=True)
            arm.set_servo_angle(angle=[0, 7, 0, 107, 0, 100, mydegrees], speed=speed, wait=True)
            arm.set_position(xLoc, yLoc, 139, 0, 0, 0, wait=True)
            # a = arm.get_inverse_kinematics([xLoc, yLoc, 135, 0, 0, 0])
            # arm.set_servo_angle(angle=a[1], speed=speed, wait=True)
            arm.set_state(state=0)
            # Grab fixture
            arm.set_gripper_position(60, wait=True)
            arm.set_state(state=0)
            # return to bird eye position
            arm.set_servo_angle(angle=birdEye, speed=speed, wait=True)
            arm.set_state(state=0)
            # move to storage location
            arm.set_servo_angle(angle=sLoc, speed=speed, wait=True)
            arm.set_state(state=0)
            # Release
            arm.set_gripper_position(800, wait=True)
            arm.set_state(state=0)
            # retract arm
            arm.set_servo_angle(servo_id=2, angle=-40, speed=speed, wait=True)
            arm.set_state(state=0)
            # Return to BirdEye before going standby
            arm.set_servo_angle(angle=birdEye, speed=speed, wait=True)
            arm.set_state(state=0)
    else:
        print("No QR or QR out of bounds")

arm.disconnect()
