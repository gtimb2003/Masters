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
#arm.reset(wait=True)

#arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0, 0], speed=100, wait=True)
#print(arm.get_inverse_kinematics([0, 50, 50, 0 ,0], input_is_radian=False, return_is_radian=False))

#arm.set_servo_angle(angle=[0, 98, 0, -83, 0, -164, 0], speed=100, wait=True)
#a=arm.get_inverse_kinematics([0, 0, 0, 0, 0, 0, 0])
#b = a[1]
#c = np.rad2deg(b)
#print(np.round(c))

#arm.reset(wait=True)

#move to point A, get IK of PointC at Point A
arm.set_position(600,0,300,0,0,0,wait=True)
#IK_pointA_C=arm.get_inverse_kinematics([307,0,112,180,0,0])
#a=arm.get_inverse_kinematics([300,0,300,0,0,0],False, False)
