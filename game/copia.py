import pygame
import random
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib


#modelo = joblib.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/model_gameTree.joblib')
modelo=load_model('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/model_game.h5')
#joblib.load('regression_model.joblib')



# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 900, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
prediccion_salto=False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []
# exec(open("C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/NN.py").read())
 
#Variables para el delay del predict
frame_predict_counter = 0
frame_predict_interval = 5 

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/sprites/mono_frame_1.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/sprites/mono_frame_2.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/sprites/mono_frame_3.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/sprites/mono_frame_4.png')
]


bala_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/game/ufo.png')
menu_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        guardar_datos()
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto,distancia,salto_hecho
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

def exporta_cv():
    df_rrss=pd.DataFrame(datos_modelo)
    df_rrss.to_csv('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/dataset.csv',index=False,sep=',')
       
# Función para obtener la predicción y tomar acción
def modo_automatico():
    global salto, en_suelo, frame_predict_counter
    if frame_predict_counter % frame_predict_interval == 0:
        distancia = abs(jugador.x - bala.x)
        entrada = np.array([[velocidad_bala, distancia]])
        #tree
        #prediccion = modelo.predict([[0.8, 0.3]])
        #if isinstance(prediccion, np.ndarray) and len(prediccion) > 0:
         #   prediccion = prediccion[0]       
        #neuronal
        prediccion = modelo.predict(entrada, verbose=0)[0][0]
        print(f"Predicción: {prediccion}")
        if prediccion > 0.5 and en_suelo:
            salto = True
            en_suelo = False
            print("salto")
    frame_predict_counter += 1

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global menu_activo,correr
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
        menu_activo = True
        mostrar_menu()
    else:
        print("Juego reanudado.")
        menu_activo = False
      
        


# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, 'G' para gráficar los datos o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 8, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_g:
                    exporta_cv()
                    exec(open("C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/grafica.py").read())
                # elif evento.key == pygame.K_t:
                #    with open("C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/decisionTree.py", encoding="utf-8") as file:
                #     exec(file.read())    
                elif evento.key == pygame.K_q:
                     if not modo_auto:
                        entrenar_modelo() 
                        exporta_cv()
                        print("Juego terminado. Datos recopilados:", datos_modelo)
                     pygame.quit()
                     exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:  
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p: 
                    pausa_juego()
                if evento.key == pygame.K_q:  
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            if modo_auto:
                modo_automatico()  
            if salto:
                manejar_salto()
            guardar_datos()
            if not bala_disparada:
                disparar_bala()
            update()
        pygame.display.flip()
        reloj.tick(30)  #

    pygame.quit()

if __name__ == "__main__":
    main()
