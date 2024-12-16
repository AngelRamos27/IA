import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el archivo CSV con las columnas especificadas
columnas = ['velocidad_bala', 'distanciaHorizontal', 'distanciaDiagonal', 
            'distanciaVertical', 'salto_hecho', 'camino_atrás', 'camino_delante']
df = pd.read_csv('data_game.csv', header=0, names=columnas, dtype=float)

# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar puntos donde ocurre un salto (salto_hecho = 1)
ax.scatter(df[df['salto_hecho'] == 1]['distanciaHorizontal'], 
           df[df['salto_hecho'] == 1]['distanciaDiagonal'], 
           df[df['salto_hecho'] == 1]['distanciaVertical'], 
           c='blue', marker='o', label='Salto')

# Graficar puntos donde se camina hacia adelante (camino_delante = 4)
ax.scatter(df[df['camino_delante'] == 3]['distanciaHorizontal'], 
           df[df['camino_delante'] == 3]['distanciaDiagonal'], 
           df[df['camino_delante'] == 3]['distanciaVertical'], 
           c='green', marker='^', label='Camino Adelante')

# Graficar puntos donde se camina hacia atrás (camino_atrás = 2)
ax.scatter(df[df['camino_atrás'] == 5]['distanciaHorizontal'], 
           df[df['camino_atrás'] == 5]['distanciaDiagonal'], 
           df[df['camino_atrás'] == 5]['distanciaVertical'], 
           c='red', marker='x', label='Camino Atrás')

# Etiquetas de los ejes
ax.set_xlabel('Distancia Horizontal')
ax.set_ylabel('Distancia Diagonal')
ax.set_zlabel('Distancia Vertical')

# Mostrar leyenda
ax.legend()

# Mostrar el gráfico
plt.show()
