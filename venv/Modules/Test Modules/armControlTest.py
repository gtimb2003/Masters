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


birdEye = [0, 3.3, 0, 116, 0, 112, 0]  # Default Birdseye view
arm.set_servo_angle(angle=birdEye, speed=50, wait=True)