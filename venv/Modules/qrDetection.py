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
filepathA = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\angle.txt"

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
        cv2.polylines(img, [pts], True, (255, 0, 0), 5)


        # barcode.rect is the rectangle that encloses the qr code
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 1)
        # pts2 contains the x,y coordinates of the corner of the QR code and the width of each side

        ################
        poly = barcode.polygon # .polygon creates an array with coordinates of each corner of the qr code

        #Take the 2 bottom corners
        xy2 = poly[2]
        x2 = int(xy2[0])
        y2 = int(xy2[1])

        xy3 = poly[3]
        x3 = int(xy3[0])
        y3 = int(xy3[1])

        # get angle of bottom
        myradians = math.atan2(y2 - y3, x2 - x3)
        mydegrees = round(math.degrees(myradians))

        #calculate the midpoint between the two bottom points
        xOut = int((x3 + x2) / 2)
        yOut = int((y3 + y2) / 2)



        ################
        # x = int(pts2[0])
        # y = int(pts2[1])
        # xW = int(pts2[2])
        # yW = int(pts2[3])
        # # Add half of the width to get center coordinates
        # xOut = round(x + (xW / 2))
        # yOut = round(y + (yW / 2))


        # Open files to store coordinates
        xFile = open(filepathX, "w+")
        yFile = open(filepathY, "w+")
        aFile = open(filepathA, "w+")

        xFile.write(str(xOut))
        yFile.write(str(yOut))
        aFile.write(str(mydegrees))

        xFile.close()
        yFile.close()
        aFile.close()

        time.sleep(1)
        print(xOut, yOut, mydegrees)

    cv2.imshow('Result', img)
    cv2.waitKey(1)
