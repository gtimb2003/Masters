import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
import pyrealsense2 as rs

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#Start RealSense pipeline and save depth frames
pipeline = rs.pipeline()
pipeline.start()
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()

#Interpolation function
def inter(Input, InputLow, InputHigh, OutputLow, OutputHigh):
    interpolate = ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow
    return (interpolate)


while True:
    #QR Reading code
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        #using polygons in order to have direction
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape(-1, 1, 2)
        cv2.polylines(img, [pts], True, (255, 0 ,255), 5)
        pts2 = barcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,(255,0,255),1)
        #pts2 contains the x,y coordinates of the corner of the QR code and the width of each side
        x = int(pts2[0])
        y = int(pts2[1])
        xW = int(pts2[2])
        yW = int(pts2[3])
        #Add half of the width to get center coordinates
        xOut = x + xW // 2
        yOut = y + yW // 2

        #Open files to store coordinates
        filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
        xFile = open(filepathX, "w+")
        filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
        yFile = open(filepathtY, "w+")
        filepathtD = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\dCoor.txt"
        dFile = open(filepathtD, "w+")

        xFile.write(str(xOut))
        yFile.write(str(yOut))

        xFile.close()
        yFile.close()

        print(xOut, yOut)


        #DEPTH STUFF
        xDe = round(inter(xOut, 0, 1280, 0, 640))
        yDe = round(inter(yOut, 0, 720, 0, 480))
        dist = depth.get_distance(xDe, yDe)
        if dist != 0:
            print(dist)
            dFile.write(str(dist))
            dFile.close()



    cv2.imshow('Result', img)
    cv2.waitKey(1)