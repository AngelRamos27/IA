import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import joblib

# Cargar el dataset
file_path = 'C:/Users/angel/OneDrive/Escritorio/IA/games/dataset.csv'
dataset = pd.read_csv(file_path, header=None)

# Verificar si hay valores NaN en el conjunto de datos
print(f"Valores NaN en el conjunto de datos: {dataset.isna().sum()}")

# Eliminar filas con NaN en la columna de etiquetas (y)
dataset = dataset.dropna(subset=[2])  # Eliminar filas donde 'y' tenga NaN

# Definir características (X) y etiquetas (y)
X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

# Verificar si hay valores NaN en y
print(f"Valores NaN en y después de la limpieza: {y.isna().sum()}")

# Asegurarse de que y contiene solo valores válidos (0 o 1 en este caso)
y = y.astype(int)  # Convertir a entero

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el clasificador de Árbol de Decisión
clf = DecisionTreeClassifier(random_state=42, max_depth=1)

# Entrenar el modelo
clf.fit(X_train, y_train)

# Hacer predicciones con el modelo entrenado
y_predict = clf.predict([[-5, 660]])[0]
print(f"Predicción para [-5, 660]: {y_predict}")

# Exportar el árbol de decisión en formato DOT para su visualización
dot_data = export_graphviz(clf, out_file=None, 
                           feature_names=['Feature 1', 'Feature 2'],  
                           class_names=['Clase 0', 'Clase 1'],  
                           filled=True, rounded=True,  
                           special_characters=True)  
joblib.dump(clf, 'C:/Users/angel/OneDrive/Escritorio/IA/pygamesc/model_gameTree.joblib')


# Crear el gráfico con graphviz
graph = graphviz.Source(dot_data)

# Mostrar el gráfico
graph.view()
