import cv2
import numpy as np

class ShapeColorCounter:
    def __init__(self):
        #mascaras
         self.color_ranges = {
            'rojo': [((0, 100, 100), (10, 255, 255)), ((160, 100, 100), (180, 255, 255))],
            'amarillo': [((20, 150, 150), (30, 255, 255))],
            'verde': [((40, 100, 100), (80, 255, 255))],  
            'azul': [((90, 100, 100), (130, 255, 255))], 
            'naranja': [((10, 100, 150), (20, 255, 255))]
        }

    def countByColor(self, imagen_path, area_minima=1000):
        imagen = cv2.imread(imagen_path)
        if imagen is None:
            raise ValueError("error")

        # Suavizar la imagen para reducir ruido
        imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)
        hsv = cv2.cvtColor(imagen_suavizada, cv2.COLOR_BGR2HSV)
        conteo_formas = {}

        for color, rangos in self.color_ranges.items():
            total_contornos = 0
            mascara_final = None

            # Generar máscara combinada para cada rango
            for lower, upper in rangos:
                mascara = cv2.inRange(hsv, np.array(lower), np.array(upper))
                if mascara_final is None:
                    mascara_final = mascara
                else:
                    mascara_final = cv2.bitwise_or(mascara_final, mascara)

            # Encontrar contornos
            contornos, _ = cv2.findContours(mascara_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filtrar contornos pequeños
            contornos_validos = [c for c in contornos if cv2.contourArea(c) >= area_minima]

            total_contornos = len(contornos_validos)
            conteo_formas[color] = total_contornos

            cv2.drawContours(imagen, contornos_validos, -1, (0, 0, 0), 2)

        #resultados
        cv2.namedWindow('Formas Detectadas', cv2.WINDOW_NORMAL)  
        cv2.resizeWindow('Formas Detectadas', 500, 500)       
        cv2.imshow('Formas Detectadas', imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        return conteo_formas

def main():
    imagen_path = r"C:\Users\angel\OneDrive\Escritorio\IA\Tareas-Trabajos\salida.jpg"
    contador = ShapeColorCounter()
    resultado = contador.countByColor(imagen_path, area_minima=1000)

    print("Colores:")
    for color, cantidad in resultado.items():
        print(f"{color}: {cantidad}")

if __name__ == "__main__":
    main()
