import pygame
import math
from queue import PriorityQueue

# Configuraciones iniciales
pygame.init()

ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")
font = pygame.font.SysFont(None, 48)
# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.padre = None

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_abierto(self):
        self.color = VERDE

    def hacer_camino(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        # Movimiento hacia abajo
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col])
        # Movimiento hacia arriba
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col])
        # Movimiento hacia la derecha
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col + 1])
        # Movimiento hacia la izquierda
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col - 1])
        # Movimiento diagonal: abajo-derecha
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col + 1])
        # Movimiento diagonal: abajo-izquierda
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col - 1])
        # Movimiento diagonal: arriba-derecha
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col + 1])
        # Movimiento diagonal: arriba-izquierda
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col - 1])

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()
        pygame.time.delay(100) 

def algoritmo_a(dibujar, grid, inicio, fin):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while not open_set.empty():
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        actual = open_set.get()[2]
        open_set_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True

        for vecino in actual.vecinos:
            temp_g_score = g_score[actual] + 1

            if temp_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino.get_pos(), fin.get_pos())
                if vecino not in open_set_hash:
                    count += 1
                    open_set.put((f_score[vecino], count, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()

        dibujar()

        if actual != inicio:
            actual.hacer_cerrado()

    return False
def display_message(message):
    text = font.render(message, True, NARANJA)
    text_rect = text.get_rect(center=(ANCHO_VENTANA // 2, 800 // 2))
    VENTANA.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
def main(ventana, ancho):
    FILAS = 9
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    if algoritmo_a(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin):
                       display_message("¡Salida encontrada!")

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
