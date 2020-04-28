import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
import time
import pyrealsense2 as rs
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Start RealSense pipeline and save depth frames
pipeline = rs.pipeline()
pipeline.start()
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()

# Variables
filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
filepathtD = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\dCoor.txt"

while True:
    # QR Reading code
    success, img = cap.read()


    # Write 0 when no QR
    xOut = 0
    yOut = 0

    xFile = open(filepathX, "w+")
    yFile = open(filepathtY, "w+")

    xFile.write(str(xOut))
    yFile.write(str(yOut))

    xFile.close()
    yFile.close()

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        # using polygons in order to have direction
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape(-1, 1, 2)
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 1)
        # pts2 contains the x,y coordinates of the corner of the QR code and the width of each side
        x = int(pts2[0])
        y = int(pts2[1])
        xW = int(pts2[2])
        yW = int(pts2[3])
        # Add half of the width to get center coordinates
        xOut = round(x + (xW / 2))
        yOut = round(y + (yW / 2))

        # dx = xOut - x
        # dy = yOut - y
        # angle = math.atan2(dy, dx)
        # print(math.degrees(angle))

        # Open files to store coordinates
        filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
        xFile = open(filepathX, "w+")
        filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
        yFile = open(filepathtY, "w+")
        # filepathtD = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\dCoor.txt"
        # dFile = open(filepathtD, "w+")

        xFile.write(str(xOut))
        yFile.write(str(yOut))

        xFile.close()
        yFile.close()

        time.sleep(1)

        print(xOut, yOut)

        # # DEPTH STUFF
        # xDe = round(inter(int(pts2[0]), 0, 1280, 0, 320))
        # yDe = round(inter(int(pts2[1]), 0, 720, 0, 240))
        # dist = depth.get_distance(xDe, yDe)
        #
        # print(dist)
        # dFile.write(str(dist))
        # dFile.close()

    cv2.imshow('Result', img)
    cv2.waitKey(1)
