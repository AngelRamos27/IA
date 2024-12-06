### Análisis del Código

Este juego en Pygame incluye disparos de balas en varias trayectorias (horizontal, vertical, diagonal) y un personaje controlado por el jugador que puede saltar para evitar colisiones. El código también incorpora un menú inicial y la capacidad de guardar datos del juego, como la velocidad y la distancia de las balas, que se exportan a un archivo CSV para su análisis.

#### 1. **Bala Horizontal**
   - **Desplazamiento de la Bala:** La bala horizontal se mueve de derecha a izquierda, comenzando en la posición `(w - 50, h - 90)` y su posición horizontal disminuye con cada cuadro.
   - **Velocidad de la Bala:** La velocidad se genera aleatoriamente entre `-8` y `-3` píxeles por cuadro al dispararse. Esto crea variación en la velocidad de la bala en cada instancia.
   - **Estado de Salto (0 o 1):** La variable `salto` indica si el jugador está en el aire o no (`1` si está saltando, `0` si está en el suelo), lo cual influye en la posibilidad de colisión.
   - **Dirección:** La dirección es siempre hacia la izquierda, representada por un decremento en la coordenada `x`.
   - **Altura:** La bala mantiene una altura constante en el eje `y` al nivel del jugador, haciéndola predecible y permitiendo que el jugador esquive al saltar en el momento adecuado.

#### 2. **Bala Vertical**
   - **Desplazamiento de la Bala:** La posición vertical de la bala cambia desde una posición inicial alta (`y > h - 50`), moviéndose hacia abajo y, en caso de colisión, se reinicia.
   - **Velocidad de la Bala:** La velocidad vertical de la bala coincide con el valor aleatorio de la bala horizontal.
   - **Altura Inicial:** La bala comienza fuera de la pantalla y se desplaza hacia abajo, simulando un disparo desde la parte superior.
   - **Estado de Salto (0 o 1):** El estado de salto es crucial, ya que la bala puede pasar por encima del jugador cuando éste está en el suelo.
   - **Dirección:** La dirección es descendente, haciendo que la bala caiga directamente hacia el jugador.

#### 3. **Bala Diagonal**
   - **Desplazamiento de la Bala:** La bala diagonal se mueve en ambos ejes, generando un desplazamiento tanto en `x` como en `y`. Esto crea una trayectoria más compleja y menos predecible.
   - **Velocidad de la Bala:** Comparte la misma velocidad que la bala horizontal y la vertical, aunque aplica esta velocidad en dos direcciones, generando un movimiento diagonal hacia el jugador.
   - **Gravedad:** Aunque la gravedad no se aplica a la bala en este código, se podría agregar para que la trayectoria diagonal sea más parabólica.
   - **Altura Inicial:** Comienza en la esquina superior derecha (`w - 50, h - 90`), simulando un disparo desde una altura que tiende hacia el jugador.
   - **Estado de Salto (0 o 1):** El salto del jugador permite evitar colisiones, pero la trayectoria diagonal lo hace menos predecible.
   - **Ángulo de Disparo:** El ángulo no se define explícitamente, pero se genera con velocidad en ambas direcciones.





##### 4 *Plantear supuestos*
Caso 1: cae bala,viene diagonal y horizontal casi choca (clase 1, salta)
Caso 2 : bala vertical muy cerca, horizontal muy cerca, viene diagonal (otra clase, retrocede, en mi caso clase 3)

Para usar decision tree hay que ponerle un número a las clases
analizar las entradas de cada bala

Supervisado: identifica las clases para entender los posibles escenarios
No supervisado:el modelo prende solo

si es un valor constante no cuenta como entrada 





#### Clases



### 1. **Salta**
## Saltar se identifica con un 1
## No saltar se identifica con un 0
## Caminar para adelante se identifica con 2
## Caminar para atrás se identifica con 4
## No caminar se identifica con 3
## Agacharse se identifica con 5
## No agacharse se identifica con 6

## variables comunes
   - Variables:
     - Distancia de cada una de las balas respecto al jugador
     - Saltó o no
     - MovAtrás o no
     - MovDelante o no
     - Agacharse o no
     - Velocidad de cada bala

   - **Escenario 1**: Las balas  h ,  v ,  d  llegan al mismo tiempo al jugador.
     - *Posibles resultados/predicciones*:
       - **Acierto al saltar**: Si las balas  h  y  v  están en la misma posición y el salto logra esquivarlas.
       - **Fallo al saltar**: Si la bala  d  tiene una parábola más alta que el salto del jugador, este podría ser alcanzado por la bala  d .
       - **Esquiva combinada**: Si al saltar se esquiva la bala  h  pero la bala  d  queda justo por debajo del punto máximo del salto.
   
   - **Escenario 2**: La bala  v  está a punto de llegar al jugador, la  h  y  d  ya están en movimiento, siendo la  v  la más cercana.
     - *Posibles resultados/predicciones*:
       - **Salto evasivo**: El jugador esquiva la  v  mientras sigue en el aire; si  h  y  d  no están alineadas con el salto, puede esquivarlas también.
       - **Salto insuficiente**: Si la parábola de  d  alcanza al jugador antes de tocar el suelo, el salto falla.
       - **Doble esquive**: El jugador esquiva tanto  v  como  h , pero necesita un segundo movimiento para esquivar  d  al aterrizar.

   - **Escenario 3**: La bala  v  está por caer detrás del jugador.
     - *Posibles resultados/predicciones*:
       - **Salto corto**: Si el salto es corto, solo esquiva la bala  h  en caso de estar al frente.
       - **Movimiento innecesario**: El salto no es necesario para evitar  v , pero puede ser útil si la  h  está por llegar.
       - **Fallo estratégico**: Si  d  tiene una trayectoria curva que termina justo al aterrizar, el jugador puede ser alcanzado por  d .

---

### 2. **Camina adelante**
   - **Escenario 1**: La bala  h  está a punto de alcanzar al jugador por la izquierda.
     - *Posibles resultados/predicciones*:
       - **Esquiva exitosa**: Si la velocidad de la caminata supera a la velocidad de la bala  h , el jugador la esquiva moviéndose hacia adelante.
       - **Alerta de bala  v **: Si  v  está cayendo al frente, el jugador debe estar atento a cambiar de estrategia.
       - **Posición peligrosa**: La bala  d  podría alcanzar al jugador si su caminata lo lleva a la posición de caída.

   - **Escenario 2**: La bala  v  va a caer en su posición inicial, y la bala  h  está en camino.
     - *Posibles resultados/predicciones*:
       - **Esquiva doble**: Caminar hacia adelante permite esquivar tanto  v  como  h , dependiendo de su velocidad.
       - **Cambio de estrategia**: Si la bala  d  va a impactar por delante del jugador, es necesario detenerse o saltar en su trayectoria final.
       - **Camino libre**: Si  d  no está en el mismo eje, el movimiento puede resultar en una esquiva exitosa.

   - **Escenario 3**: La bala  d  va a caer adelante en un arco más amplio.
     - *Posibles resultados/predicciones*:
       - **Esquiva segura**: Si la bala  d  sigue en arco amplio, el jugador puede aprovechar para acercarse o esquivar.
       - **Alerta de bala  v **: Si una segunda  v  va a caer al frente, el jugador debe moverse a una posición intermedia segura.
       - **Intercepción por  h **: Si hay más balas  h  en la ruta, el jugador podría verse alcanzado.

  

---

### 3. **Camina atrás**
   - **Escenario 1**: La bala  h  está por llegar al frente del jugador y la  v  va a caer en su posición actual.
     - *Posibles resultados/predicciones*:
       - **Esquiva de última hora**: Retroceder permite esquivar ambas, pero depende de la velocidad de  h .
       - **Fallo por parábola de  d **: Si  d  tiene una parábola más corta y cae en retroceso, puede alcanzarlo.
       - **Ajuste de posición**: Si se prevé la caída de  d , puede ser útil un salto al retroceder.

   - **Escenario 2**: La bala  d  va a caer en frente, y  v  caerá detrás del jugador.
     - *Posibles resultados/predicciones*:
       - **Esquiva segura**: El jugador puede retroceder hasta que las balas estén en trayectoria segura.
       - **Cambio de dirección**: Si la  h  vuelve por el lado contrario, será necesario detenerse o saltar.
       - **Tiempo crítico**: Si el retroceso es lento y  v  acelera, el jugador puede necesitar cambiar de estrategia.

---

### 4. **Se agacha**
   - **Escenario 1**: Bala  h  a la altura del torso y  v  a punto de caer en su posición.
     - *Posibles resultados/predicciones*:
       - **Esquiva horizontal**: El jugador esquiva la bala  h  agachándose y sigue observando la caída de  v .
       - **Posición estática**: Si la bala  d  tiene una parábola alta, el jugador puede mantener posición.
       - **Estrategia de cambio rápido**: Si  v  cambia de trayectoria, el jugador debe saltar o caminar.

   - **Escenario 2**: La bala  d  está en el punto de caída y  h  está a punto de alcanzarlo.
     - *Posibles resultados/predicciones*:
       - **Evasión parcial**: Agacharse permite esquivar la  h , pero si  d  está cerca, puede requerir un cambio inmediato.
       - **Tiempo de espera**: El jugador puede esperar para observar la dirección de  v  y actuar en consecuencia.
       - **Cambio de posición**: Si  d  no cae directo, el jugador puede desplazarse horizontalmente al agacharse.

   - **Escenario 3**: Las tres balas convergen cerca del suelo.
     - *Posibles resultados/predicciones*:
       - **Esquiva arriesgada**: Agacharse puede esquivar solo si  h  está más arriba.
       - **Alerta de impacto**: La bala  d  y  v  requieren una segunda acción después de agacharse.
       - **Riesgo de colisión**: Si  h  tiene rebote, el jugador queda expuesto y debe moverse rápido.

