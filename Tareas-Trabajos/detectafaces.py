import numpy as np
import cv2 as cv
import math 

object = cv.CascadeClassifier(r'C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    objects = object.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in objects:
       frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       frame2 = cv.resize(frame, (100, 100), interpolation=cv.INTER_AREA)
       frame3= cv.cvtColor(frame, cv.COLOR_RGB2HSV)
       mascara1 = cv.inRange(frame3, 0,0,0 )
       mascara = mascara1 
       resultado = cv.bitwise_and(frame, frame, mask=mascara)
       cv.imwrite('C:/Users/angel/Escritorio/IA/EjerciciosPy/images'+str(i)+'.jpg', resultado)
       cv.imshow('objeto', frame2)
    cv.imshow('objetos', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()