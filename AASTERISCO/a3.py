import pygame
import heapq
import math

# Configuración básica
pygame.font.init()
pygame.display.set_caption("Visualización de Nodos")
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
font = pygame.font.SysFont(None, 24)
FILAS = 10
# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)


class Nodo: # clase que definea tributos y métodos del noto
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g_cost = float('inf') #distancia del nodo actual al del inicio
        self.f_cost = float('inf') #g+h
        self.padre = None #nodo anterior

    def es_pared(self):
        return self.color == NEGRO

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        self.color = AZUL

    def hacer_abierto(self):
        self.color = VERDE

    def hacer_cerrado(self):
        self.color = ROJO

    def resetear(self):
        self.color = BLANCO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def __lt__(self, otro):
        return False

def heuristica(nodo1, nodo2, grid, penalizacion_obstaculo=10):
    x1, y1 = nodo1.fila, nodo1.col
    x2, y2 = nodo2.fila, nodo2.col

    distancia = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    if grid[x2][y2].es_pared():
        distancia *= penalizacion_obstaculo

    return distancia


def obtener_vecinos(grid, nodo): #movimientos
    vecinos = []
    fila, col = nodo.fila, nodo.col

    if fila > 0:  # Arriba
        vecino = grid[fila - 1][col]
        if not vecino.es_pared():
            vecinos.append(vecino)
    if fila < len(grid) - 1:  # Abajo
        vecino = grid[fila + 1][col]
        if not vecino.es_pared():
            vecinos.append(vecino)
    if col > 0:  # Izquierda
        vecino = grid[fila][col - 1]
        if not vecino.es_pared():
            vecinos.append(vecino)
    if col < len(grid[0]) - 1:  # Derecha
        vecino = grid[fila][col + 1]
        if not vecino.es_pared():
            vecinos.append(vecino)

    return vecinos

def reconstruir_camino(padre, inicio, fin): # camino desde el fin hasta el inicio
    actual = fin
    while actual != inicio:
        actual.hacer_camino()
        actual = padre[actual]

def a_star(ventana, grid, inicio, fin):
    abiertos = []  # lista abierta
    cerrados = set()
    heapq.heappush(abiertos, (0, inicio))

    padre = {}
    inicio.g_cost = 0
    inicio.f_cost = heuristica(inicio, fin,grid)

    while len(abiertos) > 0:
        pygame.time.delay(50)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        _, nodo_actual = heapq.heappop(abiertos) #extrae el valor menor de la lista abierta

        if nodo_actual == fin: #checa si sale llega a la salida o no y reconstruye el camino
            reconstruir_camino(padre, inicio, fin)
            fin.hacer_fin()
            inicio.hacer_inicio()
            display_message("¡Salida encontrada!")
            return True

        for vecino in obtener_vecinos(grid, nodo_actual):
            temp_g_cost = nodo_actual.g_cost + 1 #valor que se acumula

            if vecino not in cerrados and temp_g_cost < vecino.g_cost: #si el vecino no está en la lista cerrada y la g es menor
                padre[vecino] = nodo_actual
                vecino.g_cost = temp_g_cost
                vecino.f_cost = temp_g_cost + heuristica(vecino, fin,grid)

                if vecino not in abiertos: #se añade a la lista abierta
                    heapq.heappush(abiertos, (vecino.f_cost, vecino))
                else:
                    # Actualizar el nodo en la cola de prioridad
                    for i, (cost, node) in enumerate(abiertos):
                        if node == vecino:
                            abiertos[i] = (temp_g_cost, vecino)
                            heapq.heapify(abiertos)
                            break

                vecino.hacer_abierto()#accesible

        nodo_actual.hacer_cerrado() #si no a la "lista cerrada", no accesible
        cerrados.add(nodo_actual)
        dibujar(ventana, grid, FILAS, ANCHO_VENTANA)

    return False

#demás funciones para generar el tablero,mostrar el mensaje y manejar los clicks y teclas
def crear_grid(filas, ancho):
    grid = []
    gap = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, gap, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    gap = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * gap), (ancho, i * gap))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * gap, 0), (j * gap, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)

    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    gap = ancho // filas
    y, x = pos
    fila = y // gap
    col = x // gap

    return fila, col

def display_message(message):
    text = font.render(message, True, NARANJA)
    text_rect = text.get_rect(center=(ANCHO_VENTANA // 2, 800 // 2))
    VENTANA.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
def main(ventana, ancho):
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != inicio and nodo != fin:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.resetear()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and fin:
                    a_star(ventana, grid, inicio, fin)

                if evento.key == pygame.K_r:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)
                    

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
