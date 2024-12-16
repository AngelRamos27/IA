import numpy as np
import cv2 as cv

# Cargar el modelo Haar para la detección de rostros
rostro = cv.CascadeClassifier(r'C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

i = 0  
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in rostros:
        # Extraer el rostro
        frame2 = frame[y:y+h, x:x+w]
        gray_face = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        
        # Umbralización binaria
        _, binary_face = cv.threshold(gray_face, 128, 255, cv.THRESH_BINARY)
        
        # Redimensionar las imágenes
        frame3 = cv.resize(binary_face, (80, 80), interpolation=cv.INTER_AREA)
        frame2 = cv.resize(binary_face, (100, 100), interpolation=cv.INTER_AREA)
        
        # Redimensionar ambas imágenes al mismo tamaño (80x80) para poder compararlas
        frame2_resized = cv.resize(frame2, (80, 80), interpolation=cv.INTER_AREA)
        
        # Calcular la similitud
        total_pixels = frame3.size
        similar_pixels = np.sum(frame3 == frame2_resized)
        similarity_percentage = (similar_pixels / total_pixels) * 100
        
        # Mostrar las imágenes y el porcentaje de similitud
        cv.imshow('Rostro 100', frame2)
        cv.imshow('Rostro 80', frame3)
        cv.imshow('Frame', gray)
        
        print(f"Porcentaje de similitud: {similarity_percentage:.2f}%")
    
    i += 1
    k = cv.waitKey(1)
    if k == 27:  # Presiona 'ESC' para salir
        break

cap.release()
cv.destroyAllWindows()
