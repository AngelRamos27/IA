import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import pandas as pd

file_path = 'C:/Users/angel/OneDrive/Escritorio/IA/game/dataset.csv'
dataset = pd.read_csv(file_path)

X = dataset.iloc[:, :2].values  # Select the first two columns for features
y = dataset.iloc[:, 2].values.astype(int)  # Select the third column for labels

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de red neuronal multicapa
model = Sequential([ Dense(4, input_dim=2, activation="relu"),Dense(1, activation="sigmoid"),])

# Compilar el modelo
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=1000, batch_size=10, verbose=1)
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")



# Probar con un nuevo dato
nuevo_dato = np.array([[0.8, 0.3]])  # Ejemplo con características específicas
prediccion = model.predict(nuevo_dato)
print(f"Predicción para {nuevo_dato}: {prediccion[0][0]:.2f}")


model.save('C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/model_game.h5') 
print("Modelo guardado")
