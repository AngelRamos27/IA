# import numpy as np
# import cv2 as cv
# img = cv.imread('salida.jpg', 1)
# img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)
import numpy as np
import cv2 as cv

# Cargar la imagen
img = cv.imread('salida.jpg', 1)

# img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Rojo
umbral_bajo_r1 = (0, 50, 50)
umbral_alto_r1 = (10, 255, 255)
umbral_bajo_r2 = (170, 50, 50)
umbral_alto_r2 = (180, 255, 255)

# Verde
umbral_bajo_v = (35, 50, 50)
umbral_alto_v = (85, 255, 255)

#  Azul
umbral_bajo_az = (90, 50, 50)
umbral_alto_az = (130, 255, 255)

#Amarillo
umbral_bajo_a = (20, 100, 100)
umbral_alto_a = (30, 255, 255)

#  Rosa
umbral_bajo_ro = (140, 50, 50)
umbral_alto_ro = (170, 255, 255)

# Naranja
umbral_bajo_n = (10, 100, 100)
umbral_alto_n = (25, 255, 255)

#mascaras
mascara_r1 = cv.inRange(img_hsv, umbral_bajo_r1, umbral_alto_r1)
mascara_r2 = cv.inRange(img_hsv, umbral_bajo_r2, umbral_alto_r2)
mascara_rojo = cv.add(mascara_r1, mascara_r2)
mascara_verde = cv.inRange(img_hsv, umbral_bajo_v, umbral_alto_v)
mascara_azul = cv.inRange(img_hsv, umbral_bajo_az, umbral_alto_az)
mascara_amarillo = cv.inRange(img_hsv, umbral_bajo_a, umbral_alto_a)
mascara_rosa = cv.inRange(img_hsv, umbral_bajo_ro, umbral_alto_ro)
mascara_naranja = cv.inRange(img_hsv, umbral_bajo_n, umbral_alto_n)

kernel = np.ones((5, 5), np.uint8)  # Puedes ajustar el tamaño del kernel según la imagen
mascara_rojo = cv.morphologyEx(mascara_rojo, cv.MORPH_CLOSE, kernel)
mascara_verde = cv.morphologyEx(mascara_verde, cv.MORPH_CLOSE, kernel)
mascara_azul = cv.morphologyEx(mascara_azul, cv.MORPH_CLOSE, kernel)
mascara_amarillo = cv.morphologyEx(mascara_amarillo, cv.MORPH_CLOSE, kernel)
mascara_rosa = cv.morphologyEx(mascara_rosa, cv.MORPH_CLOSE, kernel)
mascara_naranja = cv.morphologyEx(mascara_naranja, cv.MORPH_CLOSE, kernel)

# Aplicar las máscaras para obtener las regiones de color
resultado_rojo = cv.bitwise_and(img, img, mask=mascara_rojo)
resultado_verde = cv.bitwise_and(img, img, mask=mascara_verde)
resultado_azul = cv.bitwise_and(img, img, mask=mascara_azul)
resultado_amarillo = cv.bitwise_and(img, img, mask=mascara_amarillo)
resultado_rosa = cv.bitwise_and(img, img, mask=mascara_rosa)
resultado_naranja = cv.bitwise_and(img, img, mask=mascara_naranja)

# Función para contar objetos de un color
def contar_objetos(mascara):
    # Encontrar contornos en la máscara
    contornos, _ = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return len(contornos)

# Contar los objetos de cada color
objetos_rojo = contar_objetos(mascara_rojo)
objetos_verde = contar_objetos(mascara_verde)
objetos_azul = contar_objetos(mascara_azul)
objetos_amarillo = contar_objetos(mascara_amarillo)
objetos_rosa = contar_objetos(mascara_rosa)
objetos_naranja = contar_objetos(mascara_naranja)

# Mostrar la cantidad de objetos detectados por color
print(f"Objetos rojos: {objetos_rojo}")
print(f"Objetos verdes: {objetos_verde}")
print(f"Objetos azules: {objetos_azul}")
print(f"Objetos amarillos: {objetos_amarillo}")
print(f"Objetos rosas: {objetos_rosa}")
print(f"Objetos naranjas: {objetos_naranja}")

# Mostrar los resultados de cada color
cv.imshow('Resultado Rojo', resultado_rojo)
cv.imshow('Resultado Verde', resultado_verde)
cv.imshow('Resultado Azul', resultado_azul)
cv.imshow('Resultado Amarillo', resultado_amarillo)
cv.imshow('Resultado Rosa', resultado_rosa)
cv.imshow('Resultado Naranja', resultado_naranja)
cv.imshow('Imagen Original', img)

cv.waitKey(0)
cv.destroyAllWindows()
