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


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
arm.reset(wait=True)

while True:
    filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
    xFile = open(filepathX, "r+")
    filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
    yFile = open(filepathtY, "r+")

    x = int(xFile.read())
    y = int(yFile.read())

    xInt = inter(x, 0, 1280, 0, 180)
    yInt = inter(y, 0, 720, -180, 180)
    print(xInt, yInt)

    arm.set_servo_angle(angle=[0, 0, 0, xInt, 0, 0, yInt], speed=100, wait=True)