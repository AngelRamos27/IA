import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Ruta al archivo CSV
file_path = 'C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/actividadTrain.csv'

# Cargar el conjunto de datos
dataset = pd.read_csv(file_path, header=None, names=['x1', 'x2', 'x3', 'y1', 'y2', 'y3'])

# Separar características (X) y etiquetas (y)
X = dataset[['x1', 'x2', 'x3']].values  # Tres características de entrada
y = dataset[['y1', 'y2', 'y3']].values  # One-hot encoding de las etiquetas

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de red neuronal multicapa
model = Sequential([
    Dense(8, input_dim=3, activation="relu"),  # Capa oculta con 8 neuronas y ReLU
    Dense(8, activation="relu"),              # Otra capa oculta con 8 neuronas
    Dense(3, activation="softmax")            # Capa de salida con 3 neuronas (softmax para clasificación multiclase)
])

# Compilar el modelo
model.compile(
    loss="categorical_crossentropy",  # Pérdida para problemas de clasificación multiclase
    optimizer="adam",                 # Optimizador Adam
    metrics=["accuracy"]              # Métrica de precisión
)

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=500, batch_size=10, verbose=1)

# Evaluar el modelo en el conjunto de prueba
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

# Guardar el modelo entrenado
model.save('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/actividadModelo.h5')
print("\nModelo guardado en 'actividadModelo.h5'.")

# Visualización de la frontera de decisión (opcional, si tienes un archivo externo para graficar)
try:
    exec(open("C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/grafica2.py").read())
except FileNotFoundError:
    print("\nArchivo 'grafica2.py' no encontrado. Asegúrate de que la visualización esté configurada correctamente.")

