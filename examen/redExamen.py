import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Generar datos aleatorios
np.random.seed(42)  
num_samples = 1000

# Generar características normalizadas (x1, x2, x3)
x1 = np.random.uniform(0, 1, num_samples)  # Historial de pagos
x2 = np.random.uniform(0, 1, num_samples)  # Ingresos mensuales
x3 = np.random.uniform(0, 1, num_samples)  # Relación deuda-ingreso

# Generar etiquetas basadas en reglas simples
def classify(x1, x2, x3):
    if x1 > 0.7 and x2 > 0.7 and x3 < 0.3:
        return [1, 0, 0]  # Riesgo Bajo
    elif x1 > 0.4 and x2 > 0.4 and x3 < 0.6:
        return [0, 1, 0]  # Riesgo Medio
    else:
        return [0, 0, 1]  # Riesgo Alto

y = np.array([classify(a, b, c) for a, b, c in zip(x1, x2, x3)])

# Crear DataFrame para guardar los datos
data = pd.DataFrame({
    'x1': x1,
    'x2': x2,
    'x3': x3,
    'y1': y[:, 0],
    'y2': y[:, 1],
    'y3': y[:, 2]
})


# Separar características (X) y etiquetas (y)
X = data[['x1', 'x2', 'x3']].values
y = data[['y1', 'y2', 'y3']].values

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de red neuronal multicapa
model = Sequential([
    Dense(8, input_dim=3, activation="relu"),  # Capa oculta con 8 neuronas y ReLU
    Dense(8, activation="relu"),              # Otra capa oculta con 8 neuronas
    Dense(3, activation="softmax")            # Capa de salida con 3 neuronas (softmax para clasificación multiclase)
])

model.compile(
    loss="categorical_crossentropy",  
    optimizer="adam",                 
    metrics=["accuracy"]              
)

history = model.fit(X_train, y_train, epochs=500, batch_size=10, verbose=1)

# Evaluar el modelo en el conjunto de prueba
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

model.save('C:/Users/angel/OneDrive/Escritorio/IA/examen/actividadModelo.h5')

# Crear un meshgrid para graficar
x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))

# Evaluar el modelo en el grid
Z = model.predict(np.c_[xx.ravel(), yy.ravel(), np.zeros_like(xx.ravel())]) 
Z = np.argmax(Z, axis=1).reshape(xx.shape)

# Graficar la frontera de decisión
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.Paired)

# Graficar los puntos originales
plt.scatter(X[:, 0], X[:, 1], c=np.argmax(y, axis=1), edgecolor='k', cmap=plt.cm.Paired)
plt.title('Frontera de decisión')
plt.xlabel('x1 (Historial de pagos)')
plt.ylabel('x2 (Ingresos mensuales)')
plt.show()
