import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
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
        x = int(pts2[0])
        y = int(pts2[1])
        xW = int(pts2[2])
        yW = int(pts2[3])
        
        xOut = x + xW // 2
        yOut = y + yW // 2

        filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
        xFile = open(filepathX, "w+")
        filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
        yFile = open(filepathtY, "w+")

        xFile.write(str(xOut))
        yFile.write(str(yOut))

        xFile.close()
        yFile.close()

        print(xOut, yOut)
    cv2.imshow('Result', img)
    cv2.waitKey(1)