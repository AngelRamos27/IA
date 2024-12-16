import pygame
import random
import pandas as pd

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 950, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, balas, nave, fondo, etc.
jugador = None
bala = None
bala_diagonal = None
bala_vertical = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

#variables movimiento jugador
movAtras = False
movDelante = False


# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/sprites/mono_frame_1.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/sprites/mono_frame_2.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/sprites/mono_frame_3.png'),
    pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/sprites/mono_frame_4.png')
]


bala_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/game/ufo.png')
menu_img = pygame.image.load('C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de las balas
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala_diagonal = pygame.Rect(w - 100, h - 90, 16, 16)
bala_vertical = pygame.Rect(jugador.x, 0, 16, 16)  # Inicia en la parte superior
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables para las balas
velocidad_bala = -10
velocidad_bala_diagonal = [-5, -5]  # Diagonal hacia abajo a la izquierda
velocidad_bala_vertical = 5         # Velocidad de caída hacia el jugador
bala_disparada = False
bala_diagonal_disparada = False
bala_vertical_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar las balas
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)
        bala_disparada = True

def disparar_bala_diagonal():
    global bala_diagonal_disparada, velocidad_bala_diagonal
    if not bala_diagonal_disparada:
        velocidad_bala_diagonal[0] = random.randint(-8, -4)  # Hacia la izquierda
        velocidad_bala_diagonal[1] = random.randint(-6, -3)  # Hacia abajo
        bala_diagonal_disparada = True

def disparar_bala_vertical():
    global bala_vertical_disparada
    if not bala_vertical_disparada:
        bala_vertical.x = jugador.x  # La bala cae desde arriba en la posición del jugador
        bala_vertical_disparada = True

# Función para reiniciar las balas
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

def reset_bala_diagonal():
    global bala_diagonal, bala_diagonal_disparada
    bala_diagonal.x = w - 100
    bala_diagonal.y = h - 90
    bala_diagonal_disparada = False

def reset_bala_vertical():
    global bala_vertical, bala_vertical_disparada
    bala_vertical.y = 0
    bala_vertical_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad

        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True
def manejar_movimiento_jugador(tecla):
    global movDelante,movAtras
    if tecla[pygame.K_LEFT] and jugador.x > 0:
        jugador.x -= 5
        movAtras= True
    if tecla[pygame.K_RIGHT] and jugador.x < w - jugador.width:
        jugador.x += 5
        movDelante = True            
# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala,bala_diagonal,bala_vertical, velocidad_bala, salto,distancia,salto_hecho
    distanciaHorizontal = abs(jugador.x - bala.x)
    distanciaDiagonal = abs(jugador.x - bala_diagonal.x)
    distanciaVertical = abs(jugador.y - bala_vertical.y)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    camino_atrás = 2 if movAtras else 3 # 2 sicaminó para atrás, 3 si no 
    camino_delante = 4 if movDelante else 5  # 4 sicaminó para adelante, 5 si no 
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distanciaHorizontal,distanciaDiagonal,distanciaVertical, salto_hecho,camino_atrás,camino_delante))

def exporta_cv():
    df_rrss=pd.DataFrame(datos_modelo)
    df_rrss.to_csv('data_game.csv',index=False,sep=',')

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")
        
def reiniciar_juego():
    global menu_activo, jugador, bala, bala_diagonal, bala_vertical, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala horizontal
    bala_diagonal.x, bala_diagonal.y = w - 50, h - 90  # Reiniciar posición de la bala diagonal
    bala_vertical.x, bala_vertical.y = jugador.x, 0  # Reiniciar posición de la bala vertical (por encima del jugador)
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    if bala_disparada:
        bala.x += velocidad_bala
    if bala.x < 0:
        reset_bala()

    if bala_diagonal_disparada:
        bala_diagonal.x += velocidad_bala_diagonal[0]
        bala_diagonal.y += velocidad_bala_diagonal[1]
    if bala_diagonal.x < 0 or bala_diagonal.y > h:
        reset_bala_diagonal()

    if bala_vertical_disparada:
        bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    pantalla.blit(bala_img, (bala.x, bala.y))
    pantalla.blit(bala_img, (bala_diagonal.x, bala_diagonal.y))
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    if jugador.colliderect(bala) or jugador.colliderect(bala_diagonal) or jugador.colliderect(bala_vertical):
        print("Colisión detectada!")
        reiniciar_juego()

# Función para manejar el movimiento horizontal del jugador

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, 'G' para gráficar los datos o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 6, h // 2))
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
                    exec(open("C:/Users/angel/OneDrive/Escritorio/IA/EjerciciosPy/pygamesc/graficaMoreB.py").read())
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función principal
def main():
    global salto, en_suelo, bala_disparada, bala_diagonal_disparada, bala_vertical_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True

    while correr:
        tecla = pygame.key.get_pressed()
        manejar_movimiento_jugador(tecla)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            if not modo_auto:
                if salto:
                    manejar_salto()
                guardar_datos()

            if not bala_disparada:
                disparar_bala()
            if not bala_diagonal_disparada:
                disparar_bala_diagonal()
            if not bala_vertical_disparada:
                disparar_bala_vertical()
            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
