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
filepathY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
filepathtD = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\dCoor.txt"

while True:
    # QR Reading code
    success, img = cap.read()

    # Write 0 when no QR
    xOut = 0
    yOut = 0

    xFile = open(filepathX, "w+")
    yFile = open(filepathY, "w+")

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

        poly = barcode.polygon

        xy0 = poly[0]
        x0 = int(xy0[0])
        y0 = int(xy0[1])

        xy1 = poly[1]
        x1 = int(xy1[0])
        y1 = (xy1[1])

        xy2 = poly[2]
        x2 = int(xy2[0])
        y2 = (xy2[1])

        xy3 = poly[3]
        x3 = int(xy3[0])
        y3 = (xy3[1])

        myradians = math.atan2(y1 - y0, x1 - x0)
        mydegrees = math.degrees(myradians)


        print(xy0, xy1, xy2, xy3)
        print(mydegrees)


    cv2.imshow('Result', img)
    cv2.waitKey(1)
