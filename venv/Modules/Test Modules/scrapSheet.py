import os
import sys
import time
import math
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


arm = XArmAPI('192.168.1.103')
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

birdEye = [0, 3.3, 0, 116, 0, 112, 0]  # Default Birdseye view
arm.set_servo_angle(angle=birdEye, speed=100, wait=True)

arm.disconnect()
