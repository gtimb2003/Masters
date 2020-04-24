import os
import sys
import time
import math
import pandas as pd
import numpy as np
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

#######################################################
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser

        parser = ConfigParser()
        parser.read('C:\\Users\\geo_t\\PycharmProjects\\xArm\\xarm\\wrapper\\robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)


########################################################

def inter(Input, InputLow, InputHigh, OutputLow, OutputHigh):
    interpolate = ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow
    return (interpolate)


def interRev(Input, InputLow, InputHigh, OutputLow, OutputHigh):
    a = ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow
    interpolate = OutputHigh - a
    return (interpolate)


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


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
# Default Birdseye view
arm.set_servo_angle(angle=[0, -70, 0, 50, 0, 95, 0], speed=150, wait=True)

while True:
    # Read the location of the QR Code
    filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
    xFile = open(filepathX, "r+")
    filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
    yFile = open(filepathtY, "r+")

    # In case of an out of range situation, multiple reads of the file can crash the code that is why I put this delay
    time.sleep(1)

    # Read File
    x = int(xFile.read())
    y = int(yFile.read())

    # Interpolate the location of the QR Code
    # xInt = round(interRev(x, 1037, 261, 350, 620))
    # yInt = round(interRev(y, 436, 158, -283, 339))

    # inverted x and y because camera and robot has different point of reference
    xInt = round(remap(y, 436, 158, 317, 592))
    yInt = round(remap(x, 1030, 350, -286, 334))

    # close the file for stability
    xFile.close()
    yFile.close()

    print(xInt, yInt)
    # arm.set_servo_angle(angle=[0, 0, 0, xInt, 0, 0, yInt], speed=100, wait=True)
    # Check if QR is within limit
    if 317 <= xInt <= 592:
        if -286 <= yInt <= 334:
            arm.set_position(xInt, yInt, 150, 0, 0, 0, speed=100, wait=True)
            arm.set_servo_angle(angle=[0, -70, 0, 50, 0, 95, 0], speed=100, wait=True)
