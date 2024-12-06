### Análisis del Modelo de Clasificación de Riesgo de Clientes

#### 2. **Entrenamiento del Modelo**
El modelo implementado optimiza los pesos (`w1`, `w2`, ..., `wn`) y el sesgo (`b`) durante el proceso de entrenamiento mediante:
- **Función de pérdida:** `categorical_crossentropy`, que mide el error en problemas de clasificación multiclase.
- **Optimizador:** `Adam`, que ajusta los parámetros del modelo utilizando gradientes calculados por retropropagación.
- **Estructura:**
  - Dos capas ocultas con 8 neuronas cada una y activación ReLU.
  - Una capa de salida con 3 neuronas y activación softmax para predecir probabilidades de cada clase.

#### 3. **Gráfica de la Frontera de Decisión**
La frontera de decisión separa a los clientes según su categoría de riesgo. Para graficarla:
- Se genera un meshgrid en dos dimensiones (por ejemplo, `x1` y `x2`).
- Se evalúa el modelo en cada punto de la cuadrícula, fijando la tercera característica (e.g., `x3 = 0`).
- Se grafican las regiones correspondientes a cada clase y los puntos del conjunto de datos.

#### 4. **¿Son los datos linealmente separables?**
Los datos no son completamente linealmente separables:
- Las reglas de clasificación generan intersecciones complejas en los bordes entre las clases.
- Ejemplos con características similares pueden pertenecer a clases distintas dependiendo de pequeños cambios.

#### 5. **¿Qué ajustes podrían hacer al modelo para mejorar la clasificación?**
- **Incrementar la capacidad del modelo:**
  - Añadir más neuronas o capas ocultas para capturar relaciones más complejas.
- **Introducir regularización:**
  - Usar `Dropout` para reducir el sobreajuste.
  - Aplicar regularización L2 a los pesos.
- **Optimizar hiperparámetros:**
  - Ajustar el tamaño del batch, la tasa de aprendizaje y el número de épocas.
- **Aumentar el conjunto de datos:**
  - Generar datos adicionales o aplicar técnicas de aumento de datos.
- **Probar diferentes arquitecturas:**
  - Explorar modelos como SVM con kernels no lineales o redes convolucionales si se representa la información espacial.

#### 6. **Describir cada una de las partes del modelo implementando**
- **Entrada:** Tres características normalizadas: `x1` (historial de pagos), `x2` (ingresos mensuales), `x3` (relación deuda-ingreso).
- **Capas ocultas:**
  - Primera capa: 8 neuronas, activación ReLU.
  - Segunda capa: 8 neuronas, activación ReLU.
- **Salida:**
  - Tres neuronas con activación softmax para clasificar en una de las tres categorías.
- **Entrenamiento:**
  - **Pérdida:** `categorical_crossentropy`.
  - **Optimizador:** Adam.
  - **Métrica:** Precisión.

