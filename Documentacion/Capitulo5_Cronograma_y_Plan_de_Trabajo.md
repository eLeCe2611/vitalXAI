# Capítulo 5: Cronograma y Plan de Trabajo

## 5.1 Marco general y objetivos de la planificación

Este capítulo recoge el programa de trabajo del proyecto: el marco temporal, el desglose de las tareas en sprints y la asignación de recursos y responsabilidades. El punto de partida es vitalXAI, la plataforma web MLOps que integra inteligencia artificial explicable para el diagnóstico asistido de neumonía mediante radiografías de tórax, definida en el capítulo de metas y propósitos. La planificación cubre los once objetivos específicos del proyecto, organizados en los bloques científico-metodológico y de ingeniería web, desde la revisión del estado del arte hasta la construcción de la interfaz clínica, el laboratorio MLOps, la seguridad y la internacionalización.

El programa de trabajo cubre el ciclo completo de concepción, implementación y documentación del sistema, y tiene un horizonte claro: la entrega y defensa del Trabajo Fin de Grado el 2 de septiembre de 2026. La ejecución se ha organizado siguiendo el marco ágil adaptado de Scrum descrito en el capítulo de gestión: las iteraciones de trabajo se aplicaron de forma plena durante la fase de implementación, mientras que las fases de planificación y de documentación se apoyaron en reuniones periódicas de seguimiento y en el tablero Kanban.

De acuerdo con el calendario real del proyecto, la planificación se articula en tres fases. La fase inicial, de finales de noviembre de 2025 a finales de febrero de 2026, estableció las bases organizativas, técnicas y documentales. La fase de desarrollo, de principios de marzo a principios de junio de 2026, concentró la implementación del sistema en siete sprints. Por último, la fase de documentación, desde principios de junio hasta septiembre de 2026, se dedicó a la elaboración de la memoria, del manual de usuario y al cierre del proyecto.

El esfuerzo total planificado asciende a 474 horas, distribuidas en nueve sprints de duración desigual que reflejan la carga real de cada bloque de trabajo: la infraestructura y el laboratorio MLOps son los bloques más pesados, mientras que la validación externa es el más contenido. Las horas de las tareas representan esfuerzo estimado, mientras que las duraciones del diagrama de Gantt representan ventanas de calendario; ambas magnitudes no se convierten mediante una jornada diaria uniforme. La dedicación efectiva varía según la fase, la naturaleza de las tareas y la participación de los asesores, tal como se detalla en la asignación de recursos del apartado 5.3. Por tanto, el cronograma debe interpretarse como una planificación temporal y de esfuerzo, no como una deducción de horas diarias constantes.

## 5.2 Desglose de tareas por Sprint

El trabajo se estructura en nueve sprints, cada uno con un propósito definido y un resultado verificable. Sus duraciones son desiguales y responden a la carga y naturaleza de cada bloque. El Sprint 0 corresponde a la fase de planificación, los siete siguientes a la fase de desarrollo y el Sprint 8 a la documentación y el cierre, de acuerdo con el calendario descrito en el capítulo de gestión.

El camino crítico del proyecto pasa por las tareas de mayor carga técnica y menor posibilidad de ejecución simultánea: la implementación del pipeline de entrenamiento de las redes convolucionales (Sprint 4) y su continuación en el pipeline Transformer (Sprint 5), necesarias antes de ejecutar el benchmarking (Sprint 8). Estas tareas concentran el mayor riesgo de desviación cronológica del proyecto. En la siguiente figura se representa la estructura de desglose del trabajo (EDT), elaborada manualmente.

*[Insertar aquí el Diagrama de Estructura de Desglose del Trabajo (EDT), elaborado manualmente]*

*Figura 2 - Diagrama EDT del proyecto*

### 5.2.1 Sprint 0 – Planificación del proyecto

Este sprint inicial cubre la preparación organizativa, técnica y documental del proyecto. Se desarrolla entre finales de noviembre de 2025 y finales de febrero de 2026, con 42 horas de esfuerzo repartidas en cuatro tareas. También incluye la revisión bibliográfica que fundamenta el estado del arte y las decisiones metodológicas posteriores.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 0.1 | Reunión inicial | Luis Carmona Berdugo, Aurelio López Fernández | 3 |
| 0.2 | Redacción del Plan de Proyecto | Luis Carmona Berdugo | 25 |
| 0.3 | Inicialización del marco tecnológico | Luis Carmona Berdugo | 8 |
| 0.4 | Cronograma en Microsoft Project | Luis Carmona Berdugo | 6 |

Tarea 0.1 – Reunión inicial: encuentro con el tutor para fijar objetivos, alcance, tecnologías (FastAPI, TensorFlow, MySQL y Groq) y metodología.

Tarea 0.2 – Redacción del Plan de Proyecto: el alumno redacta el documento marco que integra los objetivos, la organización, la metodología de gestión, el plan de tareas y la evaluación de riesgos. Esta tarea establece la base documental y metodológica de los capítulos iniciales y orienta la ejecución de los sprints posteriores.

Tarea 0.3 – Inicialización del marco tecnológico: se fijan las versiones de las librerías, se preparan los entornos virtuales de Anaconda y se crea el repositorio. Esta tarea establece el entorno de trabajo inicial y reduce el riesgo de incompatibilidades entre dependencias (riesgo R02).

Tarea 0.4 – Cronograma en Microsoft Project: se construye el diagrama de Gantt con las tareas, sus dependencias, los recursos y el camino crítico, que servirá de referencia para el seguimiento.

### 5.2.2 Sprint 1 – Infraestructura y seguridad

El primer sprint de desarrollo reúne la infraestructura y la seguridad inicial del sistema, con 70 horas de esfuerzo. En él se construyen el backend sobre FastAPI y la base de datos MySQL, se implementa la autenticación y se incorporan controles de seguridad, pruebas de compatibilidad y pruebas frente a inyección SQL. Con ocho tareas, es el sprint con más entregables del cronograma. Se desarrolla durante las dos primeras semanas de marzo de 2026 y prepara la plataforma para integrar el motor de inferencia.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 1.1 | Diseño del modelo de datos en MySQL | Luis Carmona Berdugo, Vicente de Vides Rodríguez (Consultor de Persistencia) | 10 |
| 1.2 | Backend FastAPI y conexión a la base de datos | Luis Carmona Berdugo | 14 |
| 1.3 | Registro, login y cierre de sesión | Luis Carmona Berdugo | 12 |
| 1.4 | Pantallas de autenticación | Luis Carmona Berdugo | 8 |
| 1.5 | Hashing de contraseñas y tokens de sesión | Luis Carmona Berdugo | 6 |
| 1.6 | Protección CSRF y limitación de peticiones | Luis Carmona Berdugo | 6 |
| 1.7 | Pruebas de compatibilidad de librerías y entornos | Luis Carmona Berdugo | 6 |
| 1.8 | Pruebas de seguridad e inyección SQL | Luis Carmona Berdugo | 8 |

Tarea 1.1 – Diseño del modelo de datos en MySQL: se diseña el esquema relacional del sistema, que incluye usuarios, consultas de diagnóstico, sesiones de entrenamiento, cola de trabajos y tokens de refresco. El consultor de persistencia y bases de datos aporta su criterio sobre el modelado y la optimización del esquema.

Tarea 1.2 – Backend FastAPI y conexión a la base de datos: se monta el backend con FastAPI y se configura la conexión a MySQL mediante un pool de conexiones. El renderizado de las páginas con Jinja2 y el servidor Uvicorn quedan operativos al cierre de esta tarea, sobre cuya base se construyen los endpoints posteriores del sistema.

Tarea 1.3 – Registro, login y cierre de sesión: se implementan los flujos de creación de cuenta, inicio de sesión y cierre de sesión. Las contraseñas se procesan mediante bcrypt y la sesión se gestiona mediante tokens JWT almacenados en cookies seguras, con tokens de refresco y su rotación en cada uso.

Tarea 1.4 – Pantallas de autenticación: se construyen las interfaces de login y registro con el sistema de estilos de Tailwind. El flujo completo de acceso se verifica de forma integral, desde el formulario hasta la entrada al panel.

Tarea 1.5 – Hashing de contraseñas y tokens de sesión: se integra la capa de hash de contraseñas y la emisión y validación de los tokens de sesión y de refresco.

Tarea 1.6 – Protección CSRF y limitación de peticiones: se incorpora el middleware de doble cookie frente a la falsificación de peticiones y la limitación de intentos para frenar los ataques por fuerza bruta.

Tarea 1.7 – Pruebas de compatibilidad de librerías y entornos: se ejecutan pruebas sobre los entornos virtuales de Anaconda para garantizar que las versiones de TensorFlow y Keras conviven sin conflictos antes de construir el motor de inferencia (riesgo R02).

Tarea 1.8 – Pruebas de seguridad e inyección SQL: se validan los mecanismos de autenticación y autorización y se prueban los endpoints frente a inyección SQL y exposición de datos sensibles.

### 5.2.3 Sprint 2 – Motor de diagnóstico

Este sprint desarrolla el núcleo del diagnóstico: la carga de los modelos preentrenados, el endpoint de predicción y la interfaz para subir una radiografía y consultar el resultado. Con 41 horas en tres tareas, completa la primera versión funcional del flujo de diagnóstico en la segunda mitad de marzo.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 2.1 | Carga y caché de modelos preentrenados | Luis Carmona Berdugo | 15 |
| 2.2 | Predicción y pantalla de diagnóstico | Luis Carmona Berdugo | 18 |
| 2.3 | Informe PDF del diagnóstico | Luis Carmona Berdugo | 8 |

Tarea 2.1 – Carga y caché de modelos preentrenados: se desarrolla el motor de carga de los modelos CNN y Transformer desde sus pesos. Un sistema de caché en memoria evita recargar el modelo en cada petición después de su primera carga, reduciendo el tiempo necesario para las consultas posteriores.

Tarea 2.2 – Predicción y pantalla de diagnóstico: se implementa el endpoint de predicción y la pantalla de diagnóstico en la que el facultativo sube la radiografía, selecciona la arquitectura y obtiene el diagnóstico con su nivel de confianza. El procesamiento se encola de forma asíncrona para no bloquear la interfaz durante la inferencia. Es la tarea central de este sprint: sobre ella se apoyan los mapas de explicabilidad del sprint siguiente. La pantalla presenta el resultado de forma clara y sin tecnicismos, pensando en un usuario sin formación técnica.

Tarea 2.3 – Informe PDF del diagnóstico: se implementa la generación del informe PDF que recoge la radiografía, el diagnóstico, el nivel de confianza y el modelo empleado, listo para su descarga y archivo.

### 5.2.4 Sprint 3 – Explicabilidad

Este sprint incorpora técnicas de inteligencia artificial explicable al sistema. Se implementan Saliency Maps, SmoothGrad y Grad-CAM para las CNN, además de los mapas de atención para los Transformers, y se integran en el flujo de diagnóstico. Con 48 horas repartidas en seis tareas, el sprint se desarrolla durante las dos primeras semanas de abril. La revisión del asesor de imagen médica aporta una valoración de contexto sobre las explicaciones generadas.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 3.1 | Saliency Maps | Luis Carmona Berdugo, Iván Segura Carmona | 10 |
| 3.2 | SmoothGrad | Luis Carmona Berdugo | 8 |
| 3.3 | Grad-CAM | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 3.4 | Mapas de atención | Luis Carmona Berdugo | 8 |
| 3.5 | Integración de las explicaciones en el diagnóstico | Luis Carmona Berdugo | 6 |
| 3.6 | Revisión de coherencia clínica con el asesor | Luis Carmona Berdugo, Marc Ríos Cadenas | 4 |

Tarea 3.1 – Saliency Maps: se implementa el mapa de prominencia que calcula el gradiente de la clase predicha respecto a cada píxel, resaltando las regiones más influyentes en la decisión del modelo. El asesor de deep learning y XAI revisa el cálculo.

Tarea 3.2 – SmoothGrad: se implementa la variante que promedia los mapas de saliencia sobre versiones con ruido gaussiano. El resultado es un mapa más suave y estable, en el que los patrones consistentes del modelo destacan sobre el ruido.

Tarea 3.3 – Grad-CAM: se implementan los mapas de activación de clase a partir de la última capa convolucional, que superponen a la radiografía un mapa de calor de resolución reducida. La representación puede facilitar la inspección visual por parte del profesional clínico. Se valida su correcta implementación con el asesor de deep learning y XAI.

Tarea 3.4 – Mapas de atención: se implementa la extracción de los pesos de atención de la última capa de los Transformers, promediando las cabezas de atención para obtener el mapa de relevancia de cada parche.

Tarea 3.5 – Integración de las explicaciones en el diagnóstico: se integra la generación de los mapas en el flujo de predicción, de modo que cada consulta genera automáticamente sus explicaciones.

Tarea 3.6 – Revisión de coherencia clínica con el asesor: el asesor de imagen médica revisa si los mapas apuntan a regiones pulmonares relevantes y no a artefactos.

### 5.2.5 Sprint 4 – Entrenamiento CNN

Este sprint implementa el primer pipeline de entrenamiento automatizado. Se desarrolla el script que entrena las arquitecturas convolucionales con validación cruzada de cinco pliegues y balanceo de clases, se integra con el backend para lanzar experimentos desde la plataforma y se construye el panel de seguimiento del progreso. Junto con el sprint siguiente, forma parte del camino crítico del proyecto, porque el benchmarking depende de estos pipelines. Con 52 horas en cuatro tareas, ocupa la segunda quincena de abril. El asesor de deep learning y XAI revisa el pipeline y sus métricas.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 4.1 | Script de entrenamiento con validación cruzada | Luis Carmona Berdugo, Iván Segura Carmona | 20 |
| 4.2 | Ajuste de hiperparámetros y primeras ejecuciones | Luis Carmona Berdugo | 14 |
| 4.3 | Integración del entrenamiento en el backend | Luis Carmona Berdugo | 8 |
| 4.4 | Panel de monitorización del progreso | Luis Carmona Berdugo | 10 |

Tarea 4.1 – Script de entrenamiento con validación cruzada: se implementa el script que permite entrenar las arquitecturas compatibles de tf.keras.applications con cinco pliegues estratificados y submuestreo aleatorio de la clase mayoritaria. La base preentrenada en ImageNet se mantiene congelada y se sustituye la cabeza de clasificación por una propia, con callbacks de guardado del mejor modelo, parada temprana y reducción de la tasa de aprendizaje. La estimación incluye la resolución de las incompatibilidades entre Keras y tf_keras, que consumió más tiempo del previsto. Esta tarea constituye la base del benchmarking posterior.

Tarea 4.2 – Ajuste de hiperparámetros y primeras ejecuciones: se lanzan las primeras ejecuciones sobre arquitecturas ligeras (MobileNetV2, EfficientNetB0) para calibrar el hardware y ajustar el número de épocas, el tamaño de lote y la tasa de aprendizaje. Los tiempos observados sirven para estimar mejor la duración de las tareas siguientes y valorar el alcance del benchmarking.

Tarea 4.3 – Integración del entrenamiento en el backend: se conecta el script de entrenamiento con la API, de modo que un experimento pueda lanzarse desde la plataforma y ejecutarse como un proceso independiente sin bloquear la interfaz.

Tarea 4.4 – Panel de monitorización del progreso: se construye la vista que muestra el estado del entrenamiento en tiempo real, con el progreso por modelo y la consulta del estado de la cola de trabajos. El facultativo investigador puede así seguir la evolución de sus experimentos sin salir de la plataforma.

### 5.2.6 Sprint 5 – Transformers y análisis XAI

Este sprint amplía el entrenamiento a las arquitecturas Transformer y desarrolla los módulos de análisis XAI previstos para ejecutarse después de cada entrenamiento. Forma parte del camino crítico, porque el entrenamiento de los Vision Transformers y su evaluación de explicabilidad condicionan el benchmarking previsto. Con 62 horas en seis tareas, se extiende desde finales de abril hasta el 19 de mayo. Incluye los scripts de análisis cualitativo y cuantitativo, la orquestación posterior al entrenamiento y la revisión del asesor de deep learning y XAI.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 5.1 | Script de entrenamiento de arquitecturas Transformer | Luis Carmona Berdugo, Iván Segura Carmona | 16 |
| 5.2 | Script de explicabilidad cualitativa | Luis Carmona Berdugo | 10 |
| 5.3 | Script de métricas cuantitativas y calibración | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 5.4 | Orquestación automática post-entrenamiento | Luis Carmona Berdugo | 6 |
| 5.5 | Entrenamiento de DeiT, Swin y ViT | Luis Carmona Berdugo | 14 |
| 5.6 | Revisión de resultados con el asesor de deep learning | Luis Carmona Berdugo, Iván Segura Carmona | 4 |

Tarea 5.1 – Script de entrenamiento de arquitecturas Transformer: se implementa el script que entrena DeiT, Swin-Base y ViT-384 con HuggingFace Transformers y validación cruzada de cinco pliegues, reutilizando el esquema de balanceo y de guardado de pesos del pipeline convolucional. La integración con la librería de Transformers obliga a adaptar el manejo de pesos y la tasa de aprendizaje, con ajustes específicos para lograr la convergencia. Es la tarea más exigente del sprint desde el punto de vista técnico. Su correcta ejecución era condición necesaria para el benchmarking previsto, aunque estas arquitecturas no forman parte de los resultados parciales conservados.

Tarea 5.2 – Script de explicabilidad cualitativa: se implementa el script que genera los mapas de explicabilidad visuales sobre imágenes de ejemplo, con Grad-CAM y saliencia para las CNN y saliencia para los Transformers. El resultado es la galería de mapas de cada modelo, que permite la inspección visual de la coherencia de las decisiones.

Tarea 5.3 – Script de métricas cuantitativas y calibración: se implementa el cálculo de las métricas de fidelidad de las explicaciones, Deletion AUC, Insertion AUC, Sparsity, Entropy y Stability SSIM, y de la calibración de las predicciones mediante el Expected Calibration Error y el Brier Score. La revisión del asesor de deep learning y XAI comprueba el cálculo de estas métricas.

Tarea 5.4 – Orquestación automática post-entrenamiento: se automatiza la ejecución de los análisis XAI al finalizar cada entrenamiento, de acuerdo con el flujo previsto para evaluar la explicabilidad de los modelos.

Tarea 5.5 – Entrenamiento de DeiT, Swin y ViT: se planifica el entrenamiento de las tres arquitecturas Transformer sobre el dataset. La duración de esta tarea refleja el coste computacional previsto, superior al de las CNN. Se aplican los ajustes de tasa de aprendizaje necesarios durante las ejecuciones disponibles.

Tarea 5.6 – Revisión de resultados con el asesor de deep learning: el asesor revisa la interpretación de los resultados del entrenamiento y de la explicabilidad de los Transformers.

### 5.2.7 Sprint 6 – Validación externa

Este es el sprint más breve del proyecto, con 26 horas en dos tareas y una duración de cuatro días. Implementa los mecanismos de validación externa y de análisis estadístico previstos para comparar los modelos. Se desarrolla en la segunda mitad de mayo.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 6.1 | Comparación estadística: ranking y test de Wilcoxon | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 6.2 | Validación externa y test de DeLong | Luis Carmona Berdugo | 14 |

Tarea 6.1 – Comparación estadística: ranking y análisis exploratorio: se implementa el script que genera el ranking global de los modelos por su AUC medio y calcula una matriz exploratoria de p-valores por pares. Como solo se dispone de cinco folds dependientes, el test de Wilcoxon (Wilcoxon, 1945) no se utilizará para afirmar significación confirmatoria. Cualquier contraste por pares deberá incorporar una corrección por comparaciones múltiples y sus limitaciones deberán quedar documentadas.

Tarea 6.2 – Validación externa y test de DeLong: se implementa la evaluación de los modelos congelados sobre la cohorte independiente de pacientes adultos y el test de DeLong (DeLong, DeLong, & Clarke-Pearson, 1988) para comparar las curvas ROC. La tarea aporta evidencia sobre el comportamiento de los modelos en la cohorte externa y genera las matrices de significación correspondientes.

### 5.2.8 Sprint 7 – Laboratorio MLOps

El laboratorio MLOps es, junto con la infraestructura, el bloque de mayor carga del proyecto, con 66 horas en siete tareas. Integra el asistente conversacional basado en Groq y en el modelo `openai/gpt-oss-120b`, que permite configurar y lanzar experimentos en lenguaje natural. El sprint incorpora también la cola de trabajos para diagnósticos, entrenamientos y validaciones externas, la internacionalización de la plataforma en cuatro idiomas y las vistas de resultados con el ranking, las matrices de significación y las curvas ROC. Se desarrolla en la última semana de mayo y la primera de junio.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 7.1 | Integración de la API de Groq | Luis Carmona Berdugo | 8 |
| 7.2 | Diseño del prompt del asistente | Luis Carmona Berdugo | 12 |
| 7.3 | Asistente conversacional del laboratorio | Luis Carmona Berdugo | 14 |
| 7.4 | Lanzamiento de experimentos desde el chat | Luis Carmona Berdugo | 8 |
| 7.5 | Cola de trabajos y ejecución asíncrona | Luis Carmona Berdugo | 8 |
| 7.6 | Internacionalización de la plataforma | Luis Carmona Berdugo | 8 |
| 7.7 | Vistas de resultados, rankings y curvas ROC | Luis Carmona Berdugo | 8 |

Tarea 7.1 – Integración de la API de Groq: se configura el cliente de Groq y la conexión con el modelo `openai/gpt-oss-120b` que alimenta al asistente conversacional del laboratorio.

Tarea 7.2 – Diseño del prompt del asistente: se diseña el prompt de sistema que define el comportamiento del asistente en el laboratorio MLOps. Incluye las reglas de extracción de los cinco parámetros del experimento, ruta del dataset, arquitecturas, épocas, lote y tasa de aprendizaje, y el formato JSON de salida. Es una tarea principalmente de diseño.

Tarea 7.3 – Asistente conversacional del laboratorio: se implementa el endpoint de chat y la sala de conversación, con el historial de mensajes por sesión. El asistente interpreta la configuración devuelta por el modelo y la traduce al panel del experimento, para que el usuario pueda revisarla y confirmarla.

Tarea 7.4 – Lanzamiento de experimentos desde el chat: se conecta la configuración detectada por el asistente con el lanzamiento del pipeline de entrenamiento, de modo que el experimento se encola y arranca sin escribir código.

Tarea 7.5 – Cola de trabajos y ejecución asíncrona: se implementa la cola de trabajos que gestiona los diagnósticos, los entrenamientos y las validaciones externas, con monitorización de estado y cancelación de las tareas pendientes.

Tarea 7.6 – Internacionalización de la plataforma: se incorpora el soporte multilingüe de la interfaz, los informes y el asistente en los cuatro idiomas de la plataforma, mediante atributos de traducción y diccionarios en JavaScript.

Tarea 7.7 – Vistas de resultados, rankings y curvas ROC: se construyen las vistas del laboratorio que muestran el ranking de modelos, las matrices de significación y las curvas ROC de la validación externa.

### 5.2.9 Sprint 8 – Documentación y cierre

El sprint final combina las ejecuciones parciales del benchmarking con la redacción de la memoria y del manual de usuario, las correcciones finales y la entrega. Con 67 horas en cuatro tareas, se desarrolla desde el 5 de junio hasta el 2 de septiembre de 2026. La dedicación se reparte entre la preparación y el análisis de las ejecuciones, la documentación y el cierre. La redacción de la memoria es la tarea más extensa del sprint, mientras que las correcciones y la entrega se separan en tareas específicas.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 8.1 | Ejecución parcial y análisis del benchmarking | Luis Carmona Berdugo, Iván Segura Carmona, Marc Ríos Cadenas | 18 |
| 8.2 | Redacción de la memoria y del manual de usuario | Luis Carmona Berdugo | 30 |
| 8.3 | Reunión final y correcciones | Luis Carmona Berdugo, Aurelio López Fernández | 16 |
| 8.4 | Entrega final | Luis Carmona Berdugo | 3 |

Tarea 8.1 – Ejecución parcial y análisis del benchmarking: se ejecutan y analizan ocho arquitecturas CNN con resultados conservados en el directorio del proyecto: ResNet50, DenseNet121, EfficientNetB0, EfficientNetV2B0, MobileNetV2, InceptionV3, Xception y ConvNeXtTiny. Cada una cuenta con cinco ejecuciones de validación cruzada, lo que supone cuarenta entrenamientos con sus métricas y predicciones asociadas. El banco de pruebas previsto comprendía diecinueve arquitecturas, pero los resultados de los tres Transformers y de las ocho CNN restantes no se incorporan a la ejecución documentada. Las dieciocho horas corresponden al trabajo del alumno y de los asesores para preparar los lanzamientos, revisar su configuración y analizar los resultados; el tiempo de cómputo sin supervisión directa no se contabiliza como dedicación humana. El asesor de deep learning y XAI y el asesor de imagen médica revisan la coherencia de los resultados disponibles. La reducción del alcance se documenta como consecuencia de la carga computacional identificada en el riesgo R04.

Tarea 8.2 – Redacción de la memoria y del manual de usuario: se redacta la memoria del Trabajo Fin de Grado, integrando el plan de proyecto, el análisis, el diseño, la implementación, las pruebas y las conclusiones, junto con el manual de usuario orientado a facultativos sin formación técnica. La redacción se realiza de forma incremental durante la fase de documentación y se incorporan las revisiones del tutor. Cada capítulo se elabora y revisa por separado antes de integrarlo en el documento final. El manual de usuario emplea un lenguaje no técnico y recoge capturas de los flujos principales.

Tarea 8.3 – Reunión final y correcciones: reunión con el tutor y periodo de corrección programados del 28 de agosto al 1 de septiembre. Esta tarea permite revisar el conjunto del trabajo, aplicar las correcciones detectadas, preparar la defensa y dejar la versión final lista antes de la entrega.

Tarea 8.4 – Entrega final: depósito de la memoria y de los entregables del proyecto el 2 de septiembre de 2026. Esta tarea constituye el cierre administrativo posterior a la revisión y corrección final.

## 5.3 Recursos y costes del proyecto

Este apartado detalla la asignación de recursos del proyecto. Se distinguen los recursos de trabajo, correspondientes a las personas que participan en las tareas, y los recursos materiales, que incluyen la infraestructura y el equipamiento tecnológico.

Microsoft Project centraliza la administración del proyecto. Los recursos ocasionales, como el tutor y los asesores, reciben un horario fijo; esto impide que el software reasigne automáticamente su esfuerzo ante variaciones en la duración de las tareas. Todas las asignaciones se han auditado manualmente para que la carga de los recursos laborables sea coherente con la dedicación real de cada fase del proyecto.

**Recursos de trabajo:**

- **Luis Carmona Berdugo**: asume la carga técnica integral del proyecto. Acumula 455,14 horas distribuidas a lo largo de todos los sprints. Con una tarifa estándar de 20 €/h, su esfuerzo se cuantifica en 9.102,80 €.
- **Aurelio López Fernández (tutor)**: interviene estratégicamente en los hitos de apertura (tarea 0.1) y de clausura y correcciones (tarea 8.3). Dedica 9,5 horas de supervisión a 50 €/h, sumando un total de 475,00 €.
- **Iván Segura Carmona (asesor de Deep Learning y XAI)**: participa en la revisión de las implementaciones de explicabilidad, los pipelines CNN y Transformer, la comparación estadística y el benchmarking. Acumula 5,96 horas a 50 €/h, con un total de 298,00 €.
- **Marc Ríos Cadenas (asesor de Imagen Médica)**: participa en la revisión de la coherencia de los mapas de explicabilidad y de los resultados disponibles del benchmarking. Dedica 1,9 horas a 50 €/h, sumando 95,00 €.
- **Vicente de Vides Rodríguez (consultor de persistencia y bases de datos)**: asesora sobre el diseño y la optimización de la persistencia de datos. Participa en la tarea 1.1 con 1,5 horas a 50 €/h, con un total de 75,00 €.

El coste total de los recursos de trabajo asciende, por tanto, a aproximadamente 10.045,80 €.

**Recursos materiales:**

- **Equipo de desarrollo**: se utiliza un equipo local con GPU NVIDIA compatible con CUDA, disponible para el desarrollo. El plan no especifica el modelo de GPU ni su memoria VRAM, por lo que la viabilidad de las arquitecturas con mayor resolución o capacidad no puede justificarse únicamente desde este apartado. Al tratarse de infraestructura ya disponible, no se imputa una amortización adicional al TFG.
- **Licencias de software**: coste nulo. La plataforma descansa enteramente sobre tecnologías de código abierto (Python, TensorFlow, FastAPI, MySQL), eliminando cualquier gasto de licenciamiento.
- **Servicios cloud**: no se presupuesta ningún servicio cloud en el plan base. La nube aparece únicamente como contingencia ante un fallo del equipo local, pero no existe una reserva económica asignada; si fuera necesario activarla, habría que aprobar un coste adicional o reducir el alcance del benchmarking y documentar la decisión.
- **Electricidad y API de Groq**: no se dispone de una medición o factura imputable exclusivamente al proyecto, por lo que ambos conceptos quedan fuera del presupuesto cuantificado. El consumo energético se reconoce como impacto operativo y el uso de Groq queda sujeto al plan y a las cuotas vigentes del servicio.

El coste económico documentado del proyecto asciende a **10.045,80 €**, correspondiente a los recursos humanos presupuestados. Esta cifra no debe interpretarse como un coste completo de explotación: excluye la amortización del equipo ya disponible, la electricidad, una eventual infraestructura cloud y cualquier consumo facturado de la API de Groq.

## 5.4 Reparto de responsabilidades

Este apartado recoge la distribución de responsabilidades sobre las tareas definidas en el apartado 5.2. Para cada tarea se identifica la persona responsable, los interesados que intervienen de forma puntual y la proporción asignada. El reparto porcentual recogido en las tablas del apartado 5.2 sirve de base para calcular las horas y los costes del apartado 5.3, y se relaciona con los roles definidos en la matriz RACI del capítulo de organización. El alumno desarrollador concentra la mayor parte de la carga de trabajo, mientras que los demás interesados participan de forma puntual y consultiva.

Luis Carmona Berdugo es responsable de la ejecución técnica y documental del proyecto. A lo largo de los nueve sprints acumula 455,14 horas de trabajo, que representan la mayor parte del esfuerzo planificado. Sus tareas incluyen el análisis de requisitos, el diseño de la arquitectura, la implementación del backend y la interfaz, la construcción de los pipelines de entrenamiento y los módulos XAI, el benchmarking y la documentación. En las tareas con participación de asesores, la dedicación del alumno sigue siendo mayoritaria, con porcentajes que oscilan entre el 50 % de las reuniones y el 97 % de las tareas de entrenamiento.

El carácter multidisciplinar del sistema requiere el apoyo puntual y consultivo de varios interesados. Su participación se concentra en los hitos en los que se necesita conocimiento especializado. A continuación se detalla la participación de cada uno.

Aurelio López Fernández participa como tutor académico del proyecto. Su dedicación presupuestada se concentra en la tarea 0.1, correspondiente a la reunión inicial, y en la tarea 8.3, correspondiente a la reunión final y al periodo de correcciones. En ambas comparte la dedicación al 50 % con el alumno, lo que supone 9,5 horas y un coste de 475 €. El resto del seguimiento se realiza mediante comunicaciones y revisiones puntuales que no se contabilizan como horas adicionales.

Iván Segura Carmona participa como asesor de aprendizaje profundo e inteligencia artificial explicable. Su intervención consultiva se distribuye entre los sprints técnicos: revisa las técnicas XAI en el Sprint 3, el pipeline convolucional en el Sprint 4, el entrenamiento Transformer y las métricas cuantitativas en el Sprint 5, la comparación estadística en el Sprint 6 y los resultados disponibles del benchmarking en el Sprint 8. Su dedicación total asciende a 5,96 horas, con un coste de 298 €.

Marc Ríos Cadenas interviene como asesor especialista en imagen médica. Su participación mantiene un perfil consultivo y se concentra en dos hitos que exigen criterio clínico: la revisión de la coherencia de los mapas de explicabilidad en la tarea 3.6, donde comprueba que los mapas apuntan a las regiones pulmonares relevantes y no a artefactos, y la revisión de los resultados disponibles del benchmarking en la tarea 8.1. Su dedicación, del 25% en la tarea 3.6 y del 5% en la tarea 8.1, asciende a 1,9 horas y a un coste de 95 €.

Vicente de Vides Rodríguez actúa como consultor de persistencia y bases de datos. Su intervención es puntual y estrictamente consultiva, concentrándose en la tarea 1.1, correspondiente al diseño del modelo de datos en MySQL. En ella aporta criterios sobre el modelo de persistencia y sus necesidades de almacenamiento, sin asumir la implementación, que corresponde al alumno. Su dedicación del 15 % sobre dicha tarea supone 1,5 horas y un coste de 75 €.

El resto de las partes interesadas identificadas en el capítulo de organización, como el asesor de ingeniería del software y metodología, participan únicamente a través de la matriz RACI, sin asumir tareas concretas ni horas asignadas en el cronograma del proyecto. En conjunto, el reparto refleja un trabajo académico unipersonal: la carga técnica recae principalmente en el alumno y los asesores intervienen de forma puntual. Sus costes se consolidan en el apartado 5.3.
