# Capítulo 1: Estado del Arte y Contextualización

Este capítulo presenta el estado del arte y la contextualización del Trabajo Fin de Grado titulado *"vitalXAI: Plataforma MLOps con inteligencia artificial explicable para el diagnóstico asistido de neumonía mediante radiografías de tórax"*, realizado por el alumno Luis Carmona Berdugo y tutorizado por el profesor Aurelio López Fernández. En él se introduce el problema clínico, se describen las tecnologías y métodos relevantes y se sitúa la propuesta del proyecto dentro del contexto de la inteligencia artificial aplicada al diagnóstico por imagen.

Este capítulo cumple dos funciones. Primero, presenta el problema que motiva el proyecto: la neumonía, su diagnóstico mediante radiografías de tórax y las limitaciones de los métodos actuales. Después, introduce el estado del arte de las tecnologías relacionadas con la propuesta, como la inteligencia artificial, las redes neuronales convolucionales, los Transformers, la inteligencia artificial explicable y los asistentes conversacionales basados en grandes modelos de lenguaje. Las decisiones propias de la plataforma y de su evaluación se desarrollan en los capítulos correspondientes de diseño, construcción y codificación.

## 1.1 La neumonía, un problema de salud global

La neumonía es una infección que afecta a los pulmones y, en particular, a los alvéolos, las estructuras donde se produce el intercambio de gases. La acumulación de líquido o pus en estas estructuras dificulta la llegada de oxígeno a la sangre. Entre sus manifestaciones habituales se encuentran la tos, la fiebre, la dificultad respiratoria y el dolor torácico (Torres & al., 2021).

La neumonía puede estar causada por diferentes microorganismos, siendo los más frecuentes las bacterias y los virus, aunque también existen neumonías producidas por hongos. La causa concreta condiciona el tratamiento: las neumonías bacterianas se tratan habitualmente con antibióticos, mientras que las virales no responden a estos medicamentos y requieren, en general, cuidados de soporte. Distinguir el tipo de neumonía no siempre es sencillo, y las radiografías de tórax, junto con los síntomas y las pruebas de laboratorio, son herramientas clave para orientar el diagnóstico.

La neumonía tiene una relevancia clínica y social considerable. Según la Organización Mundial de la Salud, fue responsable de aproximadamente 2,5 millones de fallecimientos en 2019 y constituye una de las principales causas de muerte por infección en el mundo (World Health Organization, 2024). Su impacto es especialmente elevado entre los grupos más vulnerables, como los menores de cinco años y las personas mayores de sesenta y cinco. En los países de ingresos bajos y medios, las dificultades de acceso a la atención sanitaria agravan especialmente la mortalidad asociada a la neumonía infantil.

La detección temprana y el diagnóstico correcto son importantes porque un retraso puede demorar el tratamiento y aumentar el riesgo de complicaciones. Sin embargo, la interpretación de una radiografía de tórax puede presentar dificultades incluso para especialistas con experiencia. Los estudios muestran variabilidad entre observadores, de modo que dos radiólogos pueden discrepar sobre la presencia de signos compatibles con neumonía (Hopstaken & al., 2004). Esta variabilidad motiva la búsqueda de herramientas informáticas que ayuden a los profesionales sanitarios a fundamentar sus decisiones, sin sustituir su valoración clínica.

## 1.2 La radiografía de tórax como imagen digital

### 1.2.1 ¿Qué es una radiografía de tórax y por qué es la prueba de referencia?

La radiografía de tórax es una prueba de imagen que utiliza rayos X para obtener una representación del interior del tórax. Los rayos X son una forma de radiación electromagnética de alta energía que atraviesa los tejidos del cuerpo en mayor o menor medida según su densidad. Los huesos, que son muy densos, absorben la mayor parte de la radiación y aparecen en la imagen de color blanco; los tejidos blandos, como el músculo o el corazón, la absorben en menor grado y se muestran en tonos grises; y las zonas llenas de aire, como los pulmones sanos, apenas la absorben y aparecen prácticamente en negro (Gonzalez & Woods, 2008).

Esta propiedad es la que permite al radiólogo detectar una neumonía: cuando los alvéolos se llenan de líquido o de pus, la zona afectada del pulmón deja de ser transparente a los rayos X y se muestra como una mancha más blanca y densa de lo normal, lo que se conoce como opacidad o infiltrado (Franquet, 2001). La radiografía de tórax es la técnica de imagen de primera línea para el diagnóstico de la neumonía porque combina tres ventajas fundamentales: es muy accesible (existe en prácticamente todos los centros sanitarios), tiene un coste bajo en comparación con otras técnicas como el TAC, y es muy rápida de adquirir. Por estos motivos, sigue siendo la herramienta estándar que se utiliza en primer lugar ante la sospecha de neumonía (Mandell & al., 2007).

### 1.2.2 ¿Cómo ve el ordenador una radiografía?

Para los algoritmos es necesario representar la radiografía como datos numéricos. Una imagen digital puede describirse como una cuadrícula de píxeles. En una radiografía en escala de grises, cada píxel contiene un valor asociado al nivel de intensidad. En una representación de 8 bits, esos valores suelen situarse entre 0 y 255. Por ejemplo, una imagen de 512 por 512 píxeles puede tratarse como una matriz de 262.144 valores (Szeliski, 2010).

Los algoritmos de visión artificial no interpretan las imágenes como lo hace una persona, sino que procesan valores organizados en estructuras matemáticas, como matrices y tensores. Las redes neuronales profundas ajustan sus parámetros para identificar patrones en esas representaciones, como se explica en las secciones siguientes.

### 1.2.3 Conjuntos de datos utilizados

Para entrenar y evaluar los modelos de inteligencia artificial es imprescindible disponer de un conjunto de imágenes etiquetadas, es decir, imágenes de las que se sabe con certeza si corresponden o no a un paciente con neumonía. En este proyecto se emplean dos conjuntos de datos públicos y anonimizados, siguiendo la metodología establecida en el estudio de referencia (Kermany & al., 2018).

El conjunto de datos de entrenamiento es el publicado por Kermany y colaboradores, procedente del Guangzhou Women and Children's Medical Center y disponible en la plataforma Kaggle. Este conjunto contiene 5.856 radiografías de tórax pediátricas en formato JPEG, clasificadas en dos categorías: NORMAL, con 1.583 imágenes, y PNEUMONIA, con 4.273 imágenes. La categoría PNEUMONIA se subdivide en neumonía bacteriana y neumonía viral. La diferencia entre el número de imágenes de ambas clases constituye un desbalanceo que se aborda más adelante en la metodología. El conjunto coincide con el utilizado en el estudio de referencia, lo que facilita la comparación contextual, aunque el protocolo experimental y las arquitecturas pueden diferir.

El segundo conjunto de datos se emplea para la validación externa, un concepto que se desarrollará en profundidad más adelante y que, de forma resumida, consiste en comprobar que los modelos funcionan también con imágenes que nunca han visto y que proceden de un entorno distinto al del entrenamiento. Este segundo conjunto es el COVID-19 Radiography Database, desarrollado por investigadores de la Universidad de Qatar y la Universidad de Dhaka (Chowdhury & al., 2020; Rahman & al., 2021). Se trata de radiografías de tórax de pacientes adultos, adquiridas con equipos y protocolos diferentes a los del dataset pediátrico de entrenamiento. De este conjunto se extraen quinientas imágenes de pacientes sanos y quinientas de pacientes con neumonía viral, garantizando así un balance perfecto entre las dos clases. La población adulta, el equipo de adquisición y los protocolos de imagen diferentes convierten esta prueba en un escenario potencialmente exigente para evaluar la capacidad de generalización de los modelos. No obstante, el conjunto combina imágenes normales y patológicas procedentes de fuentes y repositorios distintos, por lo que existe el riesgo de que un modelo aprenda señales relacionadas con el origen de la imagen en lugar de la patología (DeGrave, Janizek, & Lee, 2021).

Durante el desarrollo y la depuración se han utilizado subconjuntos reducidos de ambos conjuntos de datos para acortar los ciclos de prueba. Estos subconjuntos permiten comprobar el funcionamiento del código, pero no representan la evaluación experimental completa. La configuración del proyecto está preparada para trabajar con las 5.856 imágenes de Kermany destinadas al entrenamiento y con las 1.000 imágenes seleccionadas del COVID-19 Radiography Database para la validación externa.

## 1.3 Inteligencia Artificial, aprendizaje profundo y visión artificial

### 1.3.1 De la IA al aprendizaje profundo

La inteligencia artificial reúne técnicas que permiten a las máquinas realizar tareas asociadas habitualmente con capacidades humanas, como el aprendizaje o el reconocimiento de patrones. El aprendizaje automático es una de sus ramas y se basa en ajustar modelos a partir de ejemplos, en lugar de programar de forma explícita todas las reglas de la tarea (Bishop, 2006). En este proyecto, los ejemplos son radiografías etiquetadas y el modelo aprende una relación entre sus características visuales y las clases PNEUMONIA y NORMAL.

El aprendizaje profundo es una rama del aprendizaje automático basada en redes neuronales con múltiples capas. Cada unidad combina sus entradas mediante pesos y una función de activación. Las capas iniciales reciben la representación de la imagen y las siguientes transforman esa información hasta producir una salida relacionada con la tarea de clasificación (LeCun, Bengio, & Hinton, 2015).

El proceso mediante el que la red ajusta sus parámetros se denomina entrenamiento. De forma resumida, comprende los pasos siguientes (Goodfellow, Bengio, & Courville, 2016):

1. Propagación hacia delante: se introduce una imagen en la red y se calcula su salida con los pesos actuales.
2. Cálculo del error: se compara la salida de la red con la respuesta correcta mediante una función matemática denominada función de coste o pérdida (loss), que cuantifica cuánto se ha equivocado la red.
3. Propagación hacia atrás: se calcula cómo afectaría una pequeña variación de cada peso al error final, mediante un algoritmo llamado retropropagación del error.
4. Actualización de los pesos: se modifican ligeramente los pesos en la dirección que reduce el error, mediante un algoritmo de optimización como el descenso del gradiente.

Este ciclo se repite con todas las imágenes del conjunto de entrenamiento, y el resultado es que, progresivamente, la red va ajustando sus pesos hasta producir salidas cada vez más cercanas a las correctas. En el caso concreto de este proyecto, las redes se entrenan para resolver un problema de clasificación binaria: dada una radiografía, decidir si pertenece a la clase PNEUMONIA o a la clase NORMAL. La red no devuelve una etiqueta rígida, sino una probabilidad entre 0 y 1 (la salida de una neurona con activación sigmoide), que puede interpretarse como el nivel de confianza del modelo.

### 1.3.2 La visión artificial

La visión artificial (computer vision) es la rama de la inteligencia artificial que se ocupa de que las máquinas puedan interpretar el mundo visual: imágenes, vídeos, fotografías y, en el caso que nos ocupa, radiografías (Szeliski, 2010). La tarea concreta que aborda este proyecto es la clasificación de imágenes: asignar una categoría (en este caso, "neumonía" o "sano") a cada imagen de entrada.

La visión artificial puede apoyar el análisis de radiografías mediante modelos capaces de extraer patrones visuales y asignar una clase a cada imagen. Esta automatización no elimina la dificultad de la tarea: las radiografías presentan variaciones de adquisición y hallazgos sutiles, y el resultado del modelo debe interpretarse dentro del contexto clínico.

### 1.3.3 CheXNet y el estudio de Kermany

Para contextualizar el estado del arte se revisan dos trabajos especialmente relacionados con los datos y los modelos empleados en este proyecto.

El primero es CheXNet, presentado por Rajpurkar y colaboradores en 2017 (Rajpurkar & al., 2017). Se trata de una red convolucional de 121 capas, basada en DenseNet, entrenada con ChestX-ray14, una base de datos de más de 112.000 radiografías de unos 30.000 pacientes y con anotaciones para catorce enfermedades torácicas. El estudio comparó el rendimiento del modelo con el de un grupo de radiólogos en la detección de neumonía. Sus resultados ilustran el potencial del aprendizaje profundo en esta tarea, aunque deben interpretarse dentro de las condiciones concretas del conjunto de datos y del protocolo utilizado.

El segundo hito es el estudio de Kermany y colaboradores, publicado en la revista *Cell* en 2018 (Kermany & al., 2018), que constituye una referencia metodológica y de datos para este proyecto. El trabajo presenta un marco de aprendizaje profundo basado en transferencia de conocimiento y demuestra su aplicación a la identificación de neumonía pediátrica mediante radiografías de tórax, utilizando el conjunto de 5.856 imágenes descrito en la sección anterior. Su aportación no consiste en comparar sistemáticamente varias arquitecturas convolucionales, sino en mostrar cómo un sistema de aprendizaje profundo puede utilizarse para apoyar el diagnóstico por imagen y acompañar sus predicciones de elementos interpretables. La comparación con el rendimiento de expertos se refiere principalmente a las tareas de diagnóstico oftalmológico analizadas en el estudio, por lo que no debe trasladarse directamente a una afirmación de equivalencia entre el modelo de neumonía y los radiólogos. El artículo resulta relevante para este proyecto por el uso del dataset pediátrico, la transferencia de conocimiento y la preocupación por la interpretabilidad, pero no constituye un benchmark de cinco arquitecturas de neumonía.

Este trabajo toma ambos estudios como referencia y desarrolla una propuesta propia en tres direcciones: prepara un pipeline para comparar diecinueve arquitecturas, incorpora métricas cuantitativas de explicabilidad y calibración, y reúne el procedimiento en una plataforma web MLOps orientada a usuarios sin formación técnica. La ejecución experimental documentada es parcial y contiene resultados de ocho arquitecturas CNN. Por tanto, la aportación se presenta como la construcción de un entorno comparativo y operativo, no como una ampliación de los resultados publicados por Kermany.

## 1.4 Las redes neuronales convolucionales (CNN)

### 1.4.1 Qué es una red neuronal convolucional

Las redes neuronales convolucionales (del inglés convolutional neural networks, CNN) son el tipo de arquitectura que ha dominado históricamente la visión artificial. Su nombre procede de la operación matemática central que realizan: la convolución.

La convolución aplica filtros numéricos sobre regiones locales de la imagen. Cada filtro responde a determinados patrones, como bordes o texturas, y produce un mapa de características. El mismo filtro se aplica en distintas posiciones, lo que reduce el número de parámetros y hace que el modelo pueda reconocer un patrón con independencia de su posición exacta. Las capas de agrupación reducen la resolución espacial y resumen la información de regiones próximas (Krizhevsky, Sutskever, & Hinton, 2012).

Las CNN se estructuran en capas que extraen progresivamente características cada vez más abstractas. Las primeras capas detectan elementos sencillos como bordes y cambios de brillo; las capas intermedias combinan estos elementos en texturas y formas; y las capas finales integran el todo en conceptos de alto nivel relevantes para la tarea, en nuestro caso, la presencia o ausencia de las opacidades características de la neumonía. Entre las capas convolucionales se intercalan capas de agrupación (pooling) que reducen el tamaño de los mapas de características, condensando la información y ayudando a la red a ser más robusta y eficiente. Al final de la red, las características se aplanan y se conectan a una o varias capas densas (como las de cualquier red neuronal clásica) que producen la clasificación final.

En el contexto de este proyecto, una CNN ajusta sus parámetros para distinguir patrones visuales asociados a las clases del conjunto de entrenamiento. Esos patrones pueden incluir variaciones de densidad en los campos pulmonares, pero el modelo no garantiza que toda señal utilizada corresponda a una causa clínica relevante.

### 1.4.2 Las arquitecturas convolucionales del banco de pruebas

El proyecto contempla dieciséis arquitecturas convolucionales. Se agrupan por familias para resumir sus características principales sin reproducir una descripción exhaustiva de cada modelo. Todas parten de pesos preentrenados en ImageNet (Deng & al., 2009; Russakovsky & al., 2015). La configuración concreta del entrenamiento se documenta en la implementación del laboratorio MLOps.

**Familia ResNet** (He, Zhang, Ren, & Sun, 2016): el problema que ResNet vino a resolver es el de la degradación de las redes muy profundas. Cuando una red tiene decenas o cientos de capas, entrenarla de forma directa se vuelve extremadamente difícil, y el rendimiento, lejos de mejorar, empeora. La solución propuesta son las conexiones residuales o saltos: cada bloque de la red aprende no una transformación completa, sino la *diferencia* (el residuo) entre su entrada y su salida, sumando la entrada original. Esta idea, aparentemente sencilla, permitió entrenar redes de cientos de capas y es una de las arquitecturas más influyentes de la década. En este proyecto se evalúan:

- ResNet50: la versión de 50 capas, la más popular y equilibrada de la familia.
- ResNet101: versión más profunda (101 capas), que puede captar patrones más complejos a costa de mayor coste computacional.
- ResNet152: la más profunda de la serie (152 capas), con mayor capacidad pero también mayor demanda de recursos.
- ResNet50V2: una revisión de ResNet50 que reorganiza el orden de las operaciones dentro de cada bloque (normalizando antes de la convolución), lo que mejora el flujo de gradientes y, en general, la convergencia del entrenamiento (He, Zhang, Ren, & Sun, 2016).

**Familia DenseNet** (Huang, Liu, Van Der Maaten, & Weinberger, 2017): DenseNet lleva la idea de las conexiones a un extremo: en lugar de saltos puntuales, cada capa recibe como entrada las características de *todas* las capas anteriores, concatenándolas. Esto se denomina conectividad densa y favorece la reutilización de las características, el flujo de información y la regularización natural. DenseNet es especialmente relevante para este proyecto porque CheXNet, el sistema que igualó a los radiólogos en la detección de neumonía, se basaba precisamente en esta arquitectura (Rajpurkar & al., 2017). Se evalúan:

- DenseNet121: la versión de 121 capas, la más ligera y utilizada de la familia.
- DenseNet201: la versión más profunda (201 capas), con mayor capacidad de representación.

**Familia EfficientNet** (Tan & Le, 2019): EfficientNet plantea la pregunta de cómo escalar una red de forma óptima. En lugar de decidir a mano cuánto agrandar la profundidad, la anchura o la resolución de la imagen, propone un método de escalado compuesto que equilibra las tres dimensiones mediante un coeficiente único. El resultado es una familia de modelos que ofrece una excelente relación entre precisión y coste computacional. Se evalúan:

- EfficientNetB0: el modelo base de la familia, el más ligero.
- EfficientNetB3 y EfficientNetB7: versiones escaladas con mayor capacidad.
- EfficientNetV2S: la segunda generación de EfficientNet, que mejora la eficiencia del entrenamiento introduciendo capas de entrenamiento progresivo y ajustes en las operaciones (Tan & Le, 2021).

**Familia MobileNet** (Howard & al., 2017): MobileNet está diseñada para funcionar en dispositivos con recursos limitados, como teléfonos móviles. Su idea clave es la convolución separable por profundidad, que descompone una convolución estándar en dos operaciones más baratas, reduciendo drásticamente el número de parámetros y de operaciones sin sacrificar demasiada precisión. Se evalúan:

- MobileNetV2: segunda generación, que introduce los bloques residuales invertidos (Sandler & al., 2018).
- MobileNetV3Large: tercera generación, optimizada además con técnicas de búsqueda de arquitecturas (Howard & al., 2019).

**VGG16** (Simonyan & Zisserman, 2015): VGG mostró que una arquitectura sencilla, basada en una pila uniforme de capas convolucionales de 3×3 seguidas de capas de agrupación, podía alcanzar un rendimiento competitivo al aumentar su profundidad. Su simplicidad la convierte en un modelo de referencia para comparar arquitecturas más complejas.

**InceptionV3** (Szegedy & al., 2016): la idea de Inception es aplicar varios filtros de distinto tamaño (1×1, 3×3 y 5×5) en paralelo sobre la misma región, de modo que la red pueda captar patrones a diferentes escalas simultáneamente. InceptionV3 refina esta idea con convoluciones factorizadas que reducen el coste computacional.

**Xception** (Chollet, 2017): Xception lleva la idea de Inception al extremo y se basa exclusivamente en convoluciones separables por profundidad, demostrando que esta operación, combinada de la forma adecuada, puede superar a las arquitecturas clásicas de Inception. Es una arquitectura especialmente eficiente en términos de parámetros.

**ConvNeXtTiny** (Liu & al., 2022): ConvNeXt es una relectura moderna de las CNN: tomando como base ResNet, incorpora de forma sistemática las ideas que hicieron exitosos a los Transformers (normalizaciones, funciones de activación modernas, menor número de bloques de normalización), demostrando que las CNN "modernizadas" pueden competir con los Transformers en igualdad de condiciones. ConvNeXtTiny es la versión pequeña de esta familia.

Las dieciséis arquitecturas cubren distintas capacidades y costes computacionales, desde modelos ligeros como MobileNetV2 hasta modelos de mayor tamaño como ConvNeXt-Tiny. Esta variedad, junto con los estudios comparativos de CNN y Transformers en radiografías, proporciona un marco amplio para analizar la detección de neumonía (Murphy & al., 2022).

## 1.5 Los Transformers en visión artificial

### 1.5.1 El mecanismo de atención

Para entender los modelos más recientes de este proyecto es necesario introducir otra familia de arquitecturas: los Transformers. Su historia comienza en el procesamiento del lenguaje natural. Durante años, las tareas de lenguaje se resolvían con redes recurrentes que procesaban las palabras de una frase una a una, en orden, manteniendo un estado interno. Este enfoque era lento y tenía dificultades para recordar relaciones entre palabras muy separadas dentro del texto.

En 2017, el artículo *"Attention is all you need"* (Vaswani & al., 2017) propuso una arquitectura radicalmente distinta: el Transformer, basada en un mecanismo denominado atención. La idea esencial de la atención es que, al procesar un elemento de una secuencia (por ejemplo, una palabra), el modelo puede "prestar atención" a todos los demás elementos de la secuencia simultáneamente, ponderando cuánto influye cada uno de ellos. Así, al interpretar la palabra "neumonía" en la frase "la radiografía muestra una neumonía en el lóbulo inferior", el modelo aprende a relacionarla con "radiografía" y "lóbulo inferior" aunque estén lejos en la frase.

Dos conceptos acompañan a la atención: la autoatención, que establece relaciones entre todos los elementos de una misma secuencia (cada palabra se relaciona con todas las demás), y las cabezas de atención, que son múltiples mecanismos de atención ejecutados en paralelo, cada uno especializado en un tipo distinto de relación. Además, como el Transformer no procesa los elementos en orden, necesita incorporar una codificación posicional, una información que le indica en qué posición de la secuencia se encuentra cada elemento (Vaswani & al., 2017).

### 1.5.2 De las palabras a los píxeles

La aplicación de Transformers a imágenes requiere convertir la información espacial en una representación que el modelo pueda procesar como una secuencia. El enfoque adoptado por los Vision Transformers consiste en dividir la imagen en fragmentos y representar cada uno como un elemento de esa secuencia.

El Vision Transformer (ViT) propuesto por Dosovitskiy y colaboradores en 2021 (Dosovitskiy & al., 2021) divide la imagen en una cuadrícula de pequeños fragmentos cuadrados llamados patches (parches). Cada parche se convierte en un vector numérico mediante una transformación lineal, de forma análoga a como cada palabra se convierte en un vector que la representa. Estos vectores, llamados tokens, se introducen en un Transformer junto con su codificación posicional, de modo que el modelo aplica autoatención entre todos los parches de la imagen. Para producir la clasificación final, el ViT utiliza un token especial denominado token de clasificación, cuyo estado final después de atravesar el modelo se conecta a una capa de clasificación.

La diferencia conceptual con las CNN es profunda y muy relevante para este proyecto. Una CNN procesa la imagen de forma local y progresiva: cada neurona solo "ve" una pequeña región, y la visión global se construye capa a capa. Un Transformer, en cambio, relaciona desde la primera capa todas las regiones de la imagen entre sí, lo que le permite captar dependencias de largo alcance que a una CNN podrían pasarle desapercibidas. En el contexto de la neumonía, esto significa que un Transformer puede relacionar directamente, por ejemplo, la densidad anómala de un lóbulo pulmonar con la expansión del pulmón opuesto, sin necesidad de que esa relación emerja capa tras capa. La contrapartida es que los Transformers son muy "hambrientos de datos": necesitan grandes cantidades de imágenes para aprender correctamente y tienen un coste computacional elevado, especialmente cuando la imagen se divide en muchos parches (Dosovitskiy & al., 2021). Precisamente por eso su aplicación al ámbito médico, donde los conjuntos de datos suelen ser reducidos, exige una evaluación cuidadosa, que es uno de los objetivos de este trabajo.

### 1.5.3 Las arquitecturas Transformer del proyecto

Este proyecto evalúa tres arquitecturas basadas en atención:

- **DeiT** (Data-efficient Image Transformers) (Touvron & al., 2021): DeiT aborda directamente el problema del hambre de datos de los ViT. Su idea central es el uso de un token de destilación: durante el entrenamiento, un profesor (típicamente una CNN muy potente) "enseña" al Transformer, y el token de destilación es un elemento adicional que el modelo aprende a usar para imitar al profesor. Esto permite que un Transformer se entrene correctamente con muchos menos datos. En este proyecto se emplea la variante deit-base-distilled, preentrenada a 224×224 píxeles.
- **Swin Transformer** (Liu & al., 2021): Swin ataca el problema del coste computacional de los Transformers. En lugar de calcular la autoatención sobre todos los parches de la imagen (lo que crece de forma cuadrática con el número de parches), Swin la calcula dentro de ventanas locales, que además se desplazan entre capas consecutivas (ventanas desplazadas). Este diseño jerárquico, inspirado en las CNN, reduce el coste y permite captar información a múltiples escalas. La variante evaluada es swin-base, con parches de 4×4 y ventanas de 7×7, a resolución 224×224.
- **ViT-384**: es el Vision Transformer estándar, pero configurado para trabajar con una resolución de entrada mayor (384×384 píxeles en lugar de los 224 habituales). Trabajar con más píxeles equivale a dividir la imagen en más parches, lo que proporciona más detalle espacial al modelo (al precio de un mayor coste computacional). La variante utilizada es vit-base-patch16-384.

La inclusión de estos tres modelos permite comparar las CNN y los Transformers dentro de un mismo marco experimental, aunque no mediante un protocolo de optimización idéntico. Se mantienen comunes las particiones estratificadas, el número de pliegues, el balanceo, la aumentación, el conjunto de validación y las métricas. Las CNN utilizan una base convolucional congelada y entrenan un nuevo cabezal, mientras que los Transformers ajustan sus pesos preentrenados con una tasa de aprendizaje menor y `AdamW` (Loshchilov & Hutter, 2019). Los resultados deben interpretarse como una comparación exploratoria entre familias con protocolos adaptados, no como una atribución causal de las diferencias únicamente a la arquitectura (Murphy & al., 2022).

## 1.6 La explicabilidad: inteligencia artificial explicable

### 1.6.1 El problema de la caja negra

Los modelos de aprendizaje profundo, tanto las CNN como los Transformers, contienen numerosos parámetros cuyo ajuste no ofrece una explicación directa de cada predicción. Incluso cuando una clasificación es correcta, puede ser difícil determinar qué regiones o características de la radiografía han influido en ella. En un contexto clínico resulta necesario analizar si el modelo utiliza señales relacionadas con la patología o si su decisión puede estar condicionada por artefactos de la imagen o del conjunto de datos.

Esta cuestión es especialmente relevante en el ámbito clínico, donde las decisiones deben poder analizarse y auditarse. La inteligencia artificial explicable estudia métodos para hacer más comprensibles las decisiones de los modelos de aprendizaje automático (Holzinger & al., 2022; Linardatos, Papastefanopoulos, & Kotsiantis, 2021; Tjoa & Guan, 2020). En este proyecto, los mapas muestran las regiones que contribuyen a la salida del modelo, pero no constituyen por sí mismos una prueba de causalidad ni garantizan la validez clínica de la predicción (Rajaraman & al., 2019).

### 1.6.2 Técnicas de explicabilidad

Este proyecto utiliza tres familias de técnicas de explicabilidad:

**Mapas de prominencia o Saliency Maps** (Simonyan, Vedaldi, & Zisserman, 2014): la idea es preguntarse directamente al modelo qué píxeles de la imagen han influido más en su decisión. Para ello se calcula la derivada (el gradiente) de la salida de la red respecto a cada píxel de la imagen de entrada. Intuitivamente, el gradiente indica cómo cambiaría la predicción si se modificase un píxel concreto: si un pequeño cambio en un píxel altera mucho la decisión, ese píxel es importante. El resultado es un mapa que resalta las regiones más influyentes.

**SmoothGrad** (Smilkov & al., 2017): los mapas de saliencia crudos suelen ser muy ruidosos, con pequeñas variaciones que no tienen significado clínico. SmoothGrad mejora esta situación añadiendo ruido aleatorio a la imagen de entrada y promediando los mapas de saliencia obtenidos sobre varias versiones con ruido. El resultado es un mapa más suave y estable, en el que los patrones realmente consistentes del modelo destacan sobre el ruido.

**Grad-CAM** (Selvaraju & al., 2017): Grad-CAM produce mapas de activación de clase, que resaltan las regiones de la imagen que más contribuyen a la clase predicha. Para ello combina los mapas de características de la última capa convolucional del modelo con los gradientes de la clase predicha, ponderando cada mapa de características por su importancia. El resultado es un mapa de calor grueso y fácil de interpretar, que se superpone a la radiografía original. Grad-CAM es especialmente valioso en medicina porque sus mapas son suaves y corresponden de forma natural a las regiones anatómicas que el clínico puede inspeccionar.

Para las arquitecturas Transformer se emplea una variante complementaria: los mapas de atención, que extraen directamente los pesos de atención de la última capa del modelo. Como se explicó en la sección anterior, los Transformers deciden cuánta importancia prestar a cada parche de la imagen; esos pesos de atención indican, por tanto, qué regiones de la radiografía está "mirando" el modelo (Chefer, Gur, & Wolf, 2021). En este proyecto, los mapas de atención se obtienen promediando las cabezas de atención de la última capa.

### 1.6.3 La evaluación cuantitativa

Observar mapas de calor a simple vista es necesario, pero no es suficiente para una evaluación científica rigurosa: dos observadores pueden opinar de forma distinta sobre la calidad de un mismo mapa. Por ello, este proyecto incorpora métricas cuantitativas que puntúan de forma objetiva distintas propiedades de las explicaciones generadas. La evaluación de fidelidad mediante borrado e inserción se fundamenta en Petsiuk, Das y Saenko (2018), mientras que la consideración de medidas de concentración y complejidad se encuadra en la literatura general sobre evaluación de métodos XAI (Linardatos, Papastefanopoulos, & Kotsiantis, 2021):

- **Deletion AUC** (área bajo la curva de borrado): mide qué ocurre cuando se borran progresivamente de la imagen las regiones que el mapa considera más importantes. Si al borrarlas la predicción del modelo se degrada rápidamente, el mapa señala realmente las regiones determinantes (cuanto más baja la curva, mejor la explicación).
- **Insertion AUC** (área bajo la curva de inserción): el proceso inverso; se parte de una imagen borrosa y se van añadiendo progresivamente las regiones importantes. Si el modelo acierta pronto al incorporarlas, la explicación es buena (cuanto más alta, mejor).
- **Sparsity** (dispersión): mide si el mapa es compacto y se concentra en pocas regiones, o si por el contrario es una mancha difusa que lo abarca todo. Un buen mapa debe ser directo (Linardatos, Papastefanopoulos, & Kotsiantis, 2021).
- **Entropy** (entropía): evalúa la concentración de la información del mapa desde el punto de vista de la teoría de la información; complementa a la dispersión (Linardatos, Papastefanopoulos, & Kotsiantis, 2021).
- **Stability SSIM**: mide la consistencia de las explicaciones ante pequeñas perturbaciones de la imagen de entrada, utilizando el índice de similitud estructural SSIM (Wang & al., 2004). Un modelo estable produce mapas similares para imágenes casi idénticas.

### 1.6.4 La calibración

Existe una dimensión adicional de fiabilidad que a menudo se pasa por alto y que este proyecto incorpora como mejora respecto al estudio de referencia: la calibración. Cuando una red dice "neumonía con un 95% de confianza", ese 95% debería significar que, de cada cien casos clasificados con ese nivel de confianza, aproximadamente noventa y cinco son efectivamente neumonía. En la práctica, muchas redes modernas están mal calibradas: son demasiado optimistas, y sus probabilidades declaradas no se corresponden con su precisión real (Guo, Pleiss, Sun, & Weinberger, 2017).

La métrica estándar para medir esta desviación es el Expected Calibration Error (ECE), que cuantifica la diferencia media entre la confianza declarada por el modelo y su precisión real, agrupando las predicciones en intervalos de confianza. Complementariamente se utiliza el Brier Score, una métrica que evalúa la calidad global de las probabilidades predichas. La calibración es un aspecto crítico en entornos clínicos: una alta confianza en una predicción errónea puede tener consecuencias graves, y un sistema que sobrestima su seguridad no es clínicamente fiable. Incluir estas métricas permite evaluar no solo si los modelos aciertan, sino también si saben cuándo aciertan.

En este punto conviene aclarar, por honestidad con el lector, cómo se distribuyen las cuatro técnicas XAI entre las dos vías de uso de la plataforma. En la vía de diagnóstico de la aplicación web, el módulo de explicabilidad implementa las cuatro técnicas visuales descritas (Saliency Maps, SmoothGrad y Grad-CAM para redes convolucionales, y mapas de atención para Transformers), que se generan de forma automática en cada consulta del profesional sanitario. En la vía de laboratorio MLOps, los scripts del pipeline de entrenamiento generan los mapas de explicabilidad cualitativos (Grad-CAM y mapas de saliencia para las CNN, y mapas de saliencia para los Transformers) y calculan las métricas cuantitativas y de calibración descritas en esta sección.

## 1.7 Las barreras para la adopción clínica de la IA

A pesar del potencial de la inteligencia artificial en el diagnóstico por imagen, su adopción clínica plantea dificultades relacionadas con la transparencia, la generalización y la facilidad de uso. La primera se refiere a la dificultad de interpretar las predicciones de los modelos. vitalXAI aborda esta cuestión mediante los mapas de explicabilidad y las métricas de evaluación descritos en la sección anterior. Estos elementos aportan información adicional sobre el comportamiento del modelo, pero no sustituyen la validación clínica.

La segunda barrera es la robustez y la generalización. Un modelo puede obtener buenos resultados en las condiciones controladas del laboratorio y comportarse peor ante poblaciones, equipos o protocolos de adquisición diferentes (Nagendran & al., 2020). Por este motivo, la validación externa sobre imágenes no utilizadas durante el entrenamiento es una comprobación relevante antes de considerar un posible uso clínico (Zech & al., 2018). En este proyecto se utiliza el COVID-19 Radiography Database como fuente de imágenes adultas para explorar ese cambio de distribución.

El COVID-19 Radiography Database fue desarrollado por investigadores de la Universidad de Qatar y la Universidad de Dhaka para apoyar la investigación con radiografías de tórax (Chowdhury & al., 2020; Rahman & al., 2021). En este proyecto se utiliza como fuente de imágenes adultas para la validación externa de modelos entrenados con imágenes pediátricas. Los modelos se entrenan para distinguir neumonía de normalidad, no para detectar específicamente COVID-19. Además, la combinación de fuentes y condiciones de adquisición puede introducir señales que permitan identificar el origen de las imágenes en lugar de la patología (DeGrave, Janizek, & Lee, 2021). Por ello, los resultados de esta cohorte deben considerarse evidencia complementaria y no una demostración de generalización clínica.

La tercera barrera es la usabilidad. Muchas herramientas de investigación requieren instalar entornos, ejecutar scripts o interpretar ficheros de resultados, lo que puede dificultar su uso por profesionales sanitarios. Las prácticas MLOps buscan automatizar y organizar el ciclo de vida de los modelos, desde el entrenamiento y la validación hasta el despliegue y la monitorización (Kreuzberger, Kühl, & Hirschl, 2023). En este contexto, una interfaz que reúna estas operaciones puede reducir la carga técnica para el usuario.

vitalXAI aborda esta barrera mediante un laboratorio con asistente conversacional. El usuario puede describir en lenguaje natural la configuración del experimento y revisar los parámetros antes de lanzarlo, sin tener que escribir el código del pipeline. La interfaz no elimina la complejidad del entrenamiento, sino que la organiza y la presenta mediante operaciones orientadas al flujo de trabajo del usuario.

## 1.8 Los asistentes conversacionales y los grandes modelos de lenguaje

### 1.8.1 ¿Qué son los grandes modelos de lenguaje?

Dado que el asistente conversacional es uno de los componentes de vitalXAI, es necesario situar esta tecnología en su contexto. Los grandes modelos de lenguaje son redes neuronales basadas habitualmente en la arquitectura Transformer y entrenadas con grandes colecciones de texto. Durante el entrenamiento aprenden a predecir elementos posteriores de una secuencia, lo que les permite modelar regularidades del lenguaje y generar texto a partir de un contexto dado (Brown & al., 2020; Vaswani & al., 2017).

El entrenamiento para seguir instrucciones y responder en formato de diálogo permite adaptar estos modelos a aplicaciones conversacionales. Entre las técnicas utilizadas se encuentra el aprendizaje por refuerzo con retroalimentación humana (RLHF), aunque su aplicación concreta depende del modelo y del proveedor (Ouyang & al., 2022). En vitalXAI, el modelo de lenguaje se utiliza para extraer parámetros de configuración a partir de los mensajes del usuario y no para realizar el diagnóstico.

La aplicación de los grandes modelos de lenguaje al ámbito de la medicina es un campo de investigación muy activo. Se han publicado numerosos trabajos que exploran su uso como apoyo en tareas clínicas: responder preguntas médicas, redactar informes o asistir en el diagnóstico, con resultados prometedores pero también con advertencias importantes sobre la necesidad de validación rigurosa antes de su uso clínico (Thirunavukarasu & al., 2023; Singhal & al., 2023). En este proyecto, sin embargo, el modelo de lenguaje no desempeña funciones de diagnóstico: su papel es el de un asistente de configuración que interpreta las peticiones del usuario sobre qué experimento de entrenamiento quiere lanzar y las traduce a los parámetros técnicos que necesita el sistema.

### 1.8.2 El panorama de los modelos de lenguaje y la elección inicial de Llama 3

En el momento de desarrollo de este proyecto existen numerosos grandes modelos de lenguaje, con características muy diferentes. Por un lado están los modelos propietarios y cerrados, como GPT-4 de OpenAI, Claude de Anthropic o Gemini de Google, accesibles únicamente a través de sus APIs comerciales. Estos modelos son muy potentes, pero su código no está disponible, el usuario no puede adaptarlos ni ejecutarlos en su propia infraestructura, y su uso está sujeto a las políticas y precios de cada proveedor. Por otro lado están los modelos de acceso abierto, entre los que destacan la familia Llama de Meta y los modelos de Mistral AI, cuyos pesos son publicados y pueden descargarse y utilizarse libremente (Touvron & al., 2023; Jiang & al., 2023).

La elección inicial de Llama 3 (Meta AI, 2024) para el asistente de vitalXAI se justificaba por varias razones. En primer lugar, era un modelo de pesos abiertos, lo que se alineaba con el espíritu del proyecto: transparencia, reproducibilidad y ausencia de dependencia de un proveedor concreto. En segundo lugar, ofrecía un rendimiento competitivo con los mejores modelos propietarios en razonamiento y seguimiento de instrucciones, según las evaluaciones publicadas por el propio equipo de Meta, manteniendo un tamaño razonable (el modelo inicialmente empleado, Llama 3.3 de 70.000 millones de parámetros, ofrecía una relación calidad-coste excelente). En tercer lugar, su licencia permitía tanto el uso en investigación como el uso comercial, lo que facilitaba la eventual transferencia de la tecnología. Y en cuarto lugar, al tratarse de un modelo abierto, era posible adaptarlo o sustituirlo en el futuro sin necesidad de reescribir el sistema.

La ejecución del modelo se delega en la plataforma Groq (Groq, 2024). Groq ofrece inferencia de modelos de lenguaje a través de una API en la nube, pero con una particularidad hardware: utiliza unos chips propios denominados unidades de procesamiento de lenguaje (LPU, del inglés Language Processing Units), diseñados específicamente para ejecutar modelos de Transformer a velocidades extremadamente altas y con una latencia muy reducida, muy por debajo de la que ofrecen las GPUs convencionales. Esta velocidad es clave para la experiencia de usuario: un asistente conversacional que responde con fluidez se siente natural y cercano a lo que el usuario espera de un sistema tipo ChatGPT, mientras que un asistente lento arruinaría la sensación de conversación. Además, Groq ofrece un plan gratuito con cuotas suficientes para un proyecto académico, lo que encaja con las restricciones de coste de un Trabajo Fin de Grado.

El asistente conversacional de vitalXAI se configura con un prompt de sistema cuidadosamente diseñado (una técnica denominada prompt engineering) que define su comportamiento como experto en MLOps médico. El asistente guía al usuario, en lenguaje natural, por los cinco parámetros que definen un experimento de entrenamiento: la ruta del dataset, las arquitecturas a entrenar, el número de épocas, el tamaño de lote y la tasa de aprendizaje. Cuando el usuario ha proporcionado todos los datos, el asistente devuelve un objeto JSON estructurado con la configuración completa, que el sistema interpreta automáticamente para lanzar el pipeline de entrenamiento. El asistente está además internacionalizado en cuatro idiomas (español, inglés, chino e hindi), ampliando su accesibilidad a usuarios de distintas procedencias.

La selección concreta de tecnologías, la arquitectura de la plataforma y el procedimiento experimental se documentan en los capítulos de diseño, construcción y codificación, donde se relacionan con la implementación real del sistema.

---

## Referencias del capítulo

Apostolopoulos, I. D., & Mpesiana, T. A. (2020). Covid-19: Automatic detection from X-ray images utilizing transfer learning with convolutional neural networks. *Physical and Engineering Sciences in Medicine*, 43(2), 635-640.

Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.

Brown, T., & al., e. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33, 1877-1901.

Chefer, H., Gur, S., & Wolf, L. (2021). Transformer interpretability beyond attention visualization. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 782-791.

Chollet, F. (2017). Xception: Deep learning with depthwise separable convolutions. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 1251-1258.

Chowdhury, M. E. H., & al., e. (2020). Can AI help in screening viral and COVID-19 pneumonia? *IEEE Access*, 8, 132665-132676. https://doi.org/10.1109/ACCESS.2020.3010287

DeGrave, A. J., Janizek, J. D., & Lee, S.-I. (2021). AI for radiographic COVID-19 detection selects shortcuts over signal. *Nature Machine Intelligence*, 3, 610-619. https://doi.org/10.1038/s42256-021-00338-7

Deng, J., & al., e. (2009). ImageNet: A large-scale hierarchical image database. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 248-255.

Dosovitskiy, A., & al., e. (2021). An image is worth 16x16 words: Transformers for image recognition at scale. *International Conference on Learning Representations (ICLR)*.

Franquet, T. (2001). Imaging of pneumonia: Trends and algorithms. *European Respiratory Journal*, 18(1), 196-208.

Gonzalez, R. C., & Woods, R. E. (2008). *Digital Image Processing* (3rd ed.). Prentice Hall.

Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.

Groq. (2024). *Groq: Instant AI inference*. Obtenido de https://groq.com

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the 34th International Conference on Machine Learning*, 1321-1330.

He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 770-778.

Holzinger, A., & al., e. (2022). Explainable AI methods: A brief overview. *Lecture Notes in Computer Science*, 13200, 1-19.

Hopstaken, R. M., Witbraad, T., van Engelshoven, J. M., & Dinant, G. J. (2004). Inter-observer variation in the interpretation of chest radiographs for pneumonia in community-acquired lower respiratory tract infections. *Clinical Radiology*, 59(8), 743-752. https://doi.org/10.1016/j.crad.2004.01.011

Howard, A. G., & al., e. (2017). MobileNets: Efficient convolutional neural networks for mobile vision applications. *arXiv preprint arXiv:1704.04861*.

Howard, A., & al., e. (2019). Searching for MobileNetV3. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 1314-1324.

Huang, G., Liu, Z., Van Der Maaten, L., & Weinberger, K. Q. (2017). Densely connected convolutional networks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 4700-4708.

Jiang, A. Q., & al., e. (2023). Mistral 7B. *arXiv preprint arXiv:2310.06825*.

Kermany, D. S., & al., e. (2018). Identifying medical diagnoses and treatable diseases by image-based deep learning. *Cell*, 172(5), 1122-1131.e9. https://doi.org/10.1016/j.cell.2018.02.010

Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine learning operations (MLOps): Overview, definition, and architecture. *IEEE Access*, 11, 31866-31879. https://doi.org/10.1109/ACCESS.2023.3262138

Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems*, 25, 1097-1105.

LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. *Nature*, 521(7553), 436-444.

Linardatos, P., Papastefanopoulos, V., & Kotsiantis, S. (2021). Explainable AI: A review of machine learning interpretability methods. *Entropy*, 23(1), 18.

Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularization. *International Conference on Learning Representations (ICLR)*. Obtenido de https://arxiv.org/abs/1711.05101

Liu, Z., & al., e. (2021). Swin Transformer: Hierarchical vision transformer using shifted windows. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 10012-10022.

Liu, Z., & al., e. (2022). A ConvNet for the 2020s. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 11976-11986.

Mandell, L. A., & al., e. (2007). Infectious Diseases Society of America/American Thoracic Society consensus guidelines on the management of community-acquired pneumonia in adults. *Clinical Infectious Diseases*, 44(Supplement 2), S27-S72.

Meta AI. (2024). *Introducing Meta Llama 3: The most capable openly available LLM to date*. Obtenido de https://ai.meta.com/blog/meta-llama-3/

Minaee, S., Kafieh, R., Sonka, M., Yazdani, S., & Jamalipour Soufi, G. (2020). Deep-COVID: Predicting COVID-19 from chest X-ray images using deep transfer learning. *Medical Image Analysis*, 65, 101794. https://doi.org/10.1016/j.media.2020.101794

Murphy, Z. R., Venkatesh, K., Sulam, J., & Yi, P. H. (2022). Visual transformers and convolutional neural networks for disease classification on radiographs: A comparison of performance, sample efficiency, and hidden stratification. *Radiology: Artificial Intelligence*, 4(6), e220012. https://doi.org/10.1148/ryai.220012

Nagendran, M., Chen, Y., Lovejoy, C. A., Gordon, A. C., Komorowski, M., Harvey, H., Topol, E. J., Ioannidis, J. P. A., Collins, G. S., & Maruthappu, M. (2020). Artificial intelligence versus clinicians: Systematic review of design, reporting standards, and claims of deep learning studies. *BMJ*, 368, m689. https://doi.org/10.1136/bmj.m689

Ouyang, L., & al., e. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 35, 27730-27744.

Petsiuk, V., Das, A., & Saenko, K. (2018). RISE: Randomized input sampling for explanation of black-box models. *Proceedings of the British Machine Vision Conference*.

Rahman, T., & al., e. (2021). Exploring the effect of image enhancement techniques on COVID-19 detection using chest X-ray images. *Computers in Biology and Medicine*, 132, 104319.

Rajaraman, S., Thoma, G., Antani, S., & Candemir, S. (2019). Visualizing and explaining deep learning predictions for pneumonia detection in pediatric chest radiographs. *Medical Imaging 2019: Computer-Aided Diagnosis*, 10950, 109500S-109500S-12. https://doi.org/10.1117/12.2512752

Rajpurkar, P., & al., e. (2017). CheXNet: Radiologist-level pneumonia detection on chest X-rays with deep learning. *arXiv preprint arXiv:1711.05225*.

Russakovsky, O., & al., e. (2015). ImageNet large scale visual recognition challenge. *International Journal of Computer Vision*, 115(3), 211-252.

Sandler, M., & al., e. (2018). MobileNetV2: Inverted residuals and linear bottlenecks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 4510-4520.

Selvaraju, R. R., & al., e. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. *Proceedings of the IEEE International Conference on Computer Vision*, 618-626.

Simonyan, K., Vedaldi, A., & Zisserman, A. (2014). Deep inside convolutional networks: Visualising image classification models and saliency maps. *arXiv preprint arXiv:1312.6034*.

Simonyan, K., & Zisserman, A. (2015). Very deep convolutional networks for large-scale image recognition. *International Conference on Learning Representations (ICLR)*.

Singhal, K., & al., e. (2023). Large language models encode clinical knowledge. *Nature*, 620, 172-180.

Smilkov, D., & al., e. (2017). SmoothGrad: Removing noise by adding noise. *arXiv preprint arXiv:1706.03825*.

Szegedy, C., & al., e. (2016). Rethinking the Inception architecture for computer vision. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 2818-2826.

Szeliski, R. (2010). *Computer Vision: Algorithms and Applications*. Springer.

Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. *International Conference on Machine Learning (ICML)*, 6105-6114.

Tan, M., & Le, Q. V. (2021). EfficientNetV2: Smaller models and faster training. *International Conference on Machine Learning (ICML)*, 10096-10106.

Thirunavukarasu, A. J., & al., e. (2023). Large language models in medicine. *Nature Medicine*, 29(8), 1930-1940.

Tjoa, E., & Guan, C. (2020). A survey on explainable artificial intelligence (XAI): Toward medical XAI. *IEEE Transactions on Neural Networks and Learning Systems*, 32(11), 4793-4813.

Torres, A., & al., e. (2021). Pneumonia. *Nature Reviews Disease Primers*, 7(1), 25.

Touvron, H., & al., e. (2021). Training data-efficient image transformers & distillation through attention. *Proceedings of the 38th International Conference on Machine Learning*, 10347-10357.

Touvron, H., & al., e. (2023). Llama: Open and efficient foundation language models. *arXiv preprint arXiv:2302.13971*.

Vaswani, A., & al., e. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998-6008.

Wang, Z., & al., e. (2004). Image quality assessment: From error visibility to structural similarity. *IEEE Transactions on Image Processing*, 13(4), 600-612.

World Health Organization. (2024). *Pneumonia fact sheet*. Obtenido de https://www.who.int/news-room/fact-sheets/detail/pneumonia

Zech, J. R., Badgeley, M. A., Liu, M., Costa, A. B., Titano, J. J., & Oermann, E. K. (2018). Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study. *PLOS Medicine*, 15(11), e1002683. https://doi.org/10.1371/journal.pmed.1002683
