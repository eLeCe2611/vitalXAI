# Capítulo 5: Cronograma y Plan de Trabajo

## 5.1 Marco general y objetivos de la planificación

Este capítulo recoge el programa de trabajo del proyecto: el marco temporal en el que se desarrolla, el desglose de las tareas en sprints y la asignación de recursos y responsabilidades que lo sustentan. El punto de partida es vitalXAI, la plataforma web MLOps que integra inteligencia artificial explicable para el diagnóstico asistido de neumonía mediante radiografías de tórax, definida en el capítulo de metas y propósitos. Sobre esa base, la planificación debe dar respuesta a los once objetivos específicos del proyecto, organizados en los bloques científico-metodológico y de ingeniería web: desde la revisión del estado del arte hasta la construcción de la interfaz clínica, el laboratorio MLOps, la seguridad y la internacionalización.

El programa de trabajo cubre el ciclo completo de concepción, implementación y documentación del sistema, y tiene un horizonte claro: la entrega y defensa del Trabajo Fin de Grado el 2 de septiembre de 2026. La ejecución se ha orquestado siguiendo la metodología ágil Scrum descrita en el capítulo de gestión, adaptada a la realidad de un proyecto unipersonal: la cadencia formal de los sprints se aplicó de forma plena durante la fase de implementación, mientras que las fases de planificación y de documentación se apoyaron en reuniones periódicas de seguimiento y en el tablero Kanban.

De acuerdo con el calendario real del proyecto, la planificación se articula en tres fases. La fase inicial, de finales de noviembre de 2025 a finales de febrero de 2026, estableció las bases organizativas, técnicas y documentales. La fase de desarrollo, de principios de marzo a principios de junio de 2026, concentró la implementación del sistema en siete sprints. Por último, la fase de documentación, desde principios de junio hasta septiembre de 2026, se dedicó a la elaboración de la memoria, los manuales y el cierre del proyecto.

El esfuerzo total planificado asciende a 474 horas, distribuidas en nueve sprints de duración desigual que reflejan la carga real de cada bloque de trabajo: la infraestructura y el laboratorio MLOps son los bloques más pesados, mientras que la validación externa es el más contenido. Las horas de las tareas representan esfuerzo estimado, mientras que las duraciones del diagrama de Gantt representan ventanas de calendario; ambas magnitudes no se convierten mediante una jornada diaria uniforme. La dedicación efectiva varía según la fase, la naturaleza de las tareas y la participación de los asesores, tal como se detalla en la asignación de recursos del apartado 5.3. Por tanto, el cronograma debe interpretarse como una planificación temporal y de esfuerzo, no como una deducción de horas diarias constantes.

## 5.2 Desglose de tareas por Sprint

El trabajo se estructura en nueve sprints, cada uno con un propósito definido y un incremento verificable del sistema. Sus duraciones son desiguales y responden a la carga y naturaleza de cada bloque, aunque mantienen una secuencialidad de trabajo y puntos de revisión adaptados al marco Scrum. Ninguno comienza sin que el anterior haya cerrado formalmente su revisión y su retrospectiva. Esta estructura encaja con el calendario real descrito en el capítulo de gestión: el primer sprint corresponde a la fase de planificación, los siete siguientes a la fase de desarrollo y el último a la documentación y el cierre.

El camino crítico del proyecto discurre por las tareas de mayor carga técnica y menor paralelizabilidad: la implementación del pipeline de entrenamiento de las redes convolucionales (Sprint 4) y su prolongación en el pipeline Transformer (Sprint 5), que deben completarse antes de ejecutar el benchmarking final (Sprint 8). Ninguna de estas tareas puede iniciarse sin que la anterior haya concluido, y su ejecución concentra el mayor riesgo de desviación cronológica de todo el proyecto. En la siguiente figura se representa la estructura de desglose del trabajo (EDT), elaborada manualmente.

*[Insertar aquí el Diagrama de Estructura de Desglose del Trabajo (EDT), elaborado manualmente]*

*Figura 2 - Diagrama EDT del proyecto*

### 5.2.1 Sprint 0 – Planificación del proyecto

Este sprint inicial sienta las bases del proyecto: no hay código, solo la preparación organizativa, técnica y documental. Ocupa la fase de planificación, de finales de noviembre de 2025 a finales de febrero de 2026, con una dedicación ligera y 42 horas de esfuerzo repartidas en cuatro tareas. En este sprint se realiza también la revisión bibliográfica que fundamenta el estado del arte y las decisiones metodológicas posteriores.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 0.1 | Reunión inicial | Luis Carmona Berdugo, Aurelio López Fernández | 3 |
| 0.2 | Redacción del Plan de Proyecto | Luis Carmona Berdugo | 25 |
| 0.3 | Inicialización del marco tecnológico | Luis Carmona Berdugo | 8 |
| 0.4 | Cronograma en Microsoft Project | Luis Carmona Berdugo | 6 |

Tarea 0.1 – Reunión inicial: encuentro con el tutor para fijar objetivos, alcance, tecnologías (FastAPI, TensorFlow, MySQL y Groq) y metodología.

Tarea 0.2 – Redacción del Plan de Proyecto: el alumno redacta el Plan de Proyecto, el documento marco que integra la definición de los objetivos, la organización del proyecto, la metodología de gestión, el plan de tareas y la evaluación de riesgos. Esta tarea también fija el marco documental y metodológico sobre el que se desarrolla la revisión del estado del arte. Es la tarea más extensa de este sprint y justifica sus veinticinco horas: sobre ella se sustentan los capítulos de contextualización, organización, metodología y riesgos de esta memoria. La redacción no es un mero trámite administrativo, sino el ejercicio de concreción que da forma al alcance del sistema y a su planificación. El resultado guía la ejecución de todos los sprints posteriores y sirve de contrato frente al tutor y al tribunal.

Tarea 0.3 – Inicialización del marco tecnológico: se fijan las versiones de las librerías, se preparan los entornos virtuales de Anaconda y se crea el repositorio. Esta tarea refleja la pequeña inicialización del marco tecnológico de la fase de planificación y blinda el entorno frente a las incompatibilidades de dependencias (riesgo R02).

Tarea 0.4 – Cronograma en Microsoft Project: se construye el diagrama de Gantt con las tareas, sus dependencias, los recursos y el camino crítico, que servirá de referencia para el seguimiento.

### 5.2.2 Sprint 1 – Infraestructura y seguridad

El primer sprint de desarrollo materializa el incremento funcional inaugural del sistema y es, junto con el laboratorio MLOps, el bloque de mayor carga de todo el proyecto, con 70 horas de esfuerzo. El código cobra vida: se construye el backend sobre FastAPI, se despliega la base de datos relacional MySQL que asume la persistencia de la información, se implementa el módulo de autenticación y se sientan las bases de la seguridad transversal. Su amplitud responde a que en este sprint se concentra, además de la construcción de la infraestructura, su blindaje completo: el cifrado de contraseñas, la gestión de sesiones y tokens, la protección frente a falsificación de peticiones, la limitación de acceso, las pruebas de compatibilidad de librerías sobre los entornos de Anaconda y las pruebas de seguridad. Con ocho tareas, es el sprint con más entregables del cronograma. Se desarrolla durante las dos primeras semanas de marzo de 2026 y deja la plataforma lista para recibir el motor de inferencia.

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

Tarea 1.1 – Diseño del modelo de datos en MySQL: se diseña el esquema relacional del sistema —usuarios, consultas de diagnóstico, sesiones de entrenamiento, cola de trabajos y tokens de refresco—. El consultor de persistencia y bases de datos aporta su criterio sobre el modelado y la optimización del esquema.

Tarea 1.2 – Backend FastAPI y conexión a la base de datos: se monta el backend con FastAPI y se configura la conexión a MySQL mediante un pool de conexiones, lo que permite atender el acceso concurrente de múltiples usuarios sin degradar el rendimiento. El renderizado de las páginas con Jinja2 y el servidor Uvicorn quedan operativos al cierre de esta tarea. Sobre este esqueleto se construyen todos los endpoints posteriores del sistema.

Tarea 1.3 – Registro, login y cierre de sesión: se implementan los flujos de creación de cuenta, inicio de sesión y cierre de sesión. Las contraseñas se cifran con bcrypt y la sesión se gestiona mediante tokens JWT almacenados en cookies seguras, con tokens de refresco y su rotación en cada uso.

Tarea 1.4 – Pantallas de autenticación: se construyen las interfaces de login y registro con el sistema de estilos de Tailwind. El flujo completo de acceso se verifica de forma integral, desde el formulario hasta la entrada al panel.

Tarea 1.5 – Hashing de contraseñas y tokens de sesión: se integra la capa de cifrado de contraseñas y la emisión y validación de los tokens de sesión y de refresco.

Tarea 1.6 – Protección CSRF y limitación de peticiones: se incorpora el middleware de doble cookie frente a la falsificación de peticiones y la limitación de intentos para frenar los ataques por fuerza bruta.

Tarea 1.7 – Pruebas de compatibilidad de librerías y entornos: se ejecutan pruebas sobre los entornos virtuales de Anaconda para garantizar que las versiones de TensorFlow y Keras conviven sin conflictos antes de construir el motor de inferencia (riesgo R02).

Tarea 1.8 – Pruebas de seguridad e inyección SQL: se validan los mecanismos de autenticación y autorización y se prueban los endpoints frente a inyección SQL y exposición de datos sensibles.

### 5.2.3 Sprint 2 – Motor de diagnóstico

Este sprint construye el núcleo del diagnóstico clínico: la carga de los modelos preentrenados, el endpoint de predicción y la interfaz que permite al facultativo subir una radiografía y ver el resultado. Con 41 horas en tres tareas, cierra la primera versión funcional del flujo de diagnóstico en la segunda mitad de marzo.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 2.1 | Carga y caché de modelos preentrenados | Luis Carmona Berdugo | 15 |
| 2.2 | Predicción y pantalla de diagnóstico | Luis Carmona Berdugo | 18 |
| 2.3 | Informe PDF del diagnóstico | Luis Carmona Berdugo | 8 |

Tarea 2.1 – Carga y caché de modelos preentrenados: se desarrolla el motor de carga de los modelos CNN y Transformer desde sus pesos. Un sistema de caché en memoria evita recargar el modelo en cada petición, de modo que el primer diagnóstico de cada arquitectura carga los pesos y los siguientes son instantáneos. Esta optimización es clave para la experiencia del facultativo en la consulta.

Tarea 2.2 – Predicción y pantalla de diagnóstico: se implementa el endpoint de predicción y la pantalla de diagnóstico en la que el facultativo sube la radiografía, selecciona la arquitectura y obtiene el diagnóstico con su nivel de confianza. El procesamiento se encola de forma asíncrona para no bloquear la interfaz durante la inferencia. Es la tarea central de este sprint: sobre ella se apoyan los mapas de explicabilidad del sprint siguiente. La pantalla presenta el resultado de forma clara y sin tecnicismos, pensando en un usuario sin formación técnica.

Tarea 2.3 – Informe PDF del diagnóstico: se implementa la generación del informe PDF que recoge la radiografía, el diagnóstico, el nivel de confianza y el modelo empleado, listo para su descarga y archivo.

### 5.2.4 Sprint 3 – Explicabilidad

Este sprint incorpora la inteligencia artificial explicable al sistema. Se implementan las tres familias de técnicas visuales —Saliency Maps, SmoothGrad y Grad-CAM, además de los mapas de atención para los Transformers— y se integran en el flujo de diagnóstico, de modo que cada predicción pasa a ser una decisión verificable. Con 48 horas repartidas en seis tareas, el sprint se desarrolla a lo largo de las dos primeras semanas de abril. La revisión del asesor de imagen médica cierra el bloque garantizando la coherencia clínica de las explicaciones.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 3.1 | Saliency Maps | Luis Carmona Berdugo, Iván Segura Carmona | 10 |
| 3.2 | SmoothGrad | Luis Carmona Berdugo | 8 |
| 3.3 | Grad-CAM | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 3.4 | Mapas de atención | Luis Carmona Berdugo | 8 |
| 3.5 | Integración de las explicaciones en el diagnóstico | Luis Carmona Berdugo | 6 |
| 3.6 | Revisión de coherencia clínica con el asesor | Luis Carmona Berdugo, Marc Ríos Cadenas | 4 |

Tarea 3.1 – Saliency Maps: se implementa el mapa de prominencia que calcula el gradiente de la clase predicha respecto a cada píxel, resaltando las regiones más influyentes en la decisión del modelo. La revisión del asesor de deep learning y XAI valida la corrección del cálculo.

Tarea 3.2 – SmoothGrad: se implementa la variante que promedia los mapas de saliencia sobre versiones con ruido gaussiano. El resultado es un mapa más suave y estable, en el que los patrones consistentes del modelo destacan sobre el ruido.

Tarea 3.3 – Grad-CAM: se implementan los mapas de activación de clase a partir de la última capa convolucional, que superponen a la radiografía un mapa de calor grueso y fácil de interpretar. Su suavidad y su correspondencia con las regiones anatómicas lo convierten en la técnica más valiosa para el profesional clínico. Se valida su correcta implementación con el asesor de deep learning y XAI.

Tarea 3.4 – Mapas de atención: se implementa la extracción de los pesos de atención de la última capa de los Transformers, promediando las cabezas de atención para obtener el mapa de relevancia de cada parche.

Tarea 3.5 – Integración de las explicaciones en el diagnóstico: se integra la generación de los mapas en el flujo de predicción, de modo que cada consulta genera automáticamente sus explicaciones.

Tarea 3.6 – Revisión de coherencia clínica con el asesor: el asesor de imagen médica comprueba que los mapas apuntan a las regiones pulmonares relevantes y no a artefactos.

### 5.2.5 Sprint 4 – Entrenamiento CNN

Este sprint implementa el primer pipeline de entrenamiento automatizado. Se desarrolla el script que entrena las arquitecturas convolucionales con validación cruzada de cinco pliegues y balanceo de clases, se integra con el backend para poder lanzar experimentos desde la plataforma y se construye el panel de monitorización del progreso. Es, junto con el sprint siguiente, el corazón del camino crítico del proyecto: sin el pipeline de entrenamiento no existe benchmarking posible. Con 52 horas en cuatro tareas, ocupa la segunda quincena de abril. El asesor de deep learning y XAI revisa la corrección del pipeline y de sus métricas.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 4.1 | Script de entrenamiento con validación cruzada | Luis Carmona Berdugo, Iván Segura Carmona | 20 |
| 4.2 | Ajuste de hiperparámetros y primeras ejecuciones | Luis Carmona Berdugo | 14 |
| 4.3 | Integración del entrenamiento en el backend | Luis Carmona Berdugo | 8 |
| 4.4 | Panel de monitorización del progreso | Luis Carmona Berdugo | 10 |

Tarea 4.1 – Script de entrenamiento con validación cruzada: se implementa el script que entrena dinámicamente cualquier arquitectura de tf.keras.applications con cinco pliegues estratificados y submuestreo aleatorio de la clase mayoritaria. La base preentrenada en ImageNet se mantiene congelada y se sustituye la cabeza de clasificación por una propia, con callbacks de guardado del mejor modelo, parada temprana y reducción de la tasa de aprendizaje. La estimación incluye la resolución de las incompatibilidades entre Keras y tf_keras, que consumió más tiempo del previsto. Es la tarea más costosa del sprint y la base de todo el benchmarking posterior.

Tarea 4.2 – Ajuste de hiperparámetros y primeras ejecuciones: se lanzan las primeras ejecuciones sobre arquitecturas ligeras (MobileNetV2, EfficientNetB0) para calibrar el hardware y ajustar el número de épocas, el tamaño de lote y la tasa de aprendizaje. Esta fase acumula experiencia sobre los tiempos reales de entrenamiento y permite estimar con realismo la duración de los sprints siguientes. Es un paso previo imprescindible antes de liberar a las arquitecturas más pesadas.

Tarea 4.3 – Integración del entrenamiento en el backend: se conecta el script de entrenamiento con la API, de modo que un experimento pueda lanzarse desde la plataforma y ejecutarse como un proceso independiente sin bloquear la interfaz.

Tarea 4.4 – Panel de monitorización del progreso: se construye la vista que muestra el estado del entrenamiento en tiempo real, con el progreso por modelo y la consulta del estado de la cola de trabajos. El facultativo investigador puede así seguir la evolución de sus experimentos sin salir de la plataforma.

### 5.2.6 Sprint 5 – Transformers y análisis XAI

Este sprint amplía el marco de entrenamiento a las arquitecturas Transformer y desarrolla los módulos de análisis XAI que se ejecutan automáticamente tras cada entrenamiento. Es el segundo bloque del camino crítico del proyecto: el entrenamiento de los Vision Transformers y la evaluación de su explicabilidad condicionan directamente el benchmarking final. Con 62 horas en seis tareas, el sprint se extiende desde finales de abril hasta el 19 de mayo, con el entrenamiento de DeiT, Swin-Base y ViT-384 prolongándose hasta mediados de mayo y la revisión final del asesor realizándose el 18 de mayo. Incluye la implementación de los scripts de análisis cualitativo y cuantitativo, la orquestación automática que garantiza que ningún modelo quede sin su evaluación de explicabilidad y la revisión final del asesor de deep learning y XAI sobre los resultados.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 5.1 | Script de entrenamiento de arquitecturas Transformer | Luis Carmona Berdugo, Iván Segura Carmona | 16 |
| 5.2 | Script de explicabilidad cualitativa | Luis Carmona Berdugo | 10 |
| 5.3 | Script de métricas cuantitativas y calibración | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 5.4 | Orquestación automática post-entrenamiento | Luis Carmona Berdugo | 6 |
| 5.5 | Entrenamiento de DeiT, Swin y ViT | Luis Carmona Berdugo | 14 |
| 5.6 | Revisión de resultados con el asesor de deep learning | Luis Carmona Berdugo, Iván Segura Carmona | 4 |

Tarea 5.1 – Script de entrenamiento de arquitecturas Transformer: se implementa el script que entrena DeiT, Swin-Base y ViT-384 con HuggingFace Transformers y validación cruzada de cinco pliegues, reutilizando el esquema de balanceo y de guardado de pesos del pipeline convolucional. La integración con la librería de Transformers obliga a adaptar el manejo de pesos y la tasa de aprendizaje, con ajustes específicos para lograr la convergencia. Es la tarea más exigente del sprint desde el punto de vista técnico. Su correcta ejecución es condición necesaria para el benchmarking final.

Tarea 5.2 – Script de explicabilidad cualitativa: se implementa el script que genera los mapas de explicabilidad visuales sobre imágenes de ejemplo, con Grad-CAM y saliencia para las CNN y saliencia para los Transformers. El resultado es la galería de mapas de cada modelo, que permite la inspección visual de la coherencia de las decisiones.

Tarea 5.3 – Script de métricas cuantitativas y calibración: se implementa el cálculo de las métricas de fidelidad de las explicaciones —Deletion AUC, Insertion AUC, Sparsity, Entropy y Stability SSIM— y de la calibración de las predicciones mediante el Expected Calibration Error y el Brier Score. La revisión del asesor de deep learning y XAI valida el cálculo de estas métricas.

Tarea 5.4 – Orquestación automática post-entrenamiento: se automatiza la ejecución de los análisis XAI al finalizar cada entrenamiento, garantizando que ningún modelo quede sin su evaluación de explicabilidad.

Tarea 5.5 – Entrenamiento de DeiT, Swin y ViT: se ejecuta el entrenamiento completo de las tres arquitecturas Transformer sobre el dataset. La duración de esta tarea en el cronograma refleja el coste computacional real de entrenar los Transformers, sensiblemente mayor que el de las CNN. Se aplican los ajustes de tasa de aprendizaje necesarios para lograr la convergencia de los tres modelos.

Tarea 5.6 – Revisión de resultados con el asesor de deep learning: el asesor valida la interpretación de los resultados del entrenamiento y de la explicabilidad de los Transformers.

### 5.2.7 Sprint 6 – Validación externa

Este es el sprint más contenido del proyecto, con 26 horas en dos tareas y una duración de cuatro días. Implementa los mecanismos de validación externa y de análisis estadístico que determinan si las diferencias entre modelos son reales o fruto del azar. Se desarrolla en la segunda mitad de mayo.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 6.1 | Comparación estadística: ranking y test de Wilcoxon | Luis Carmona Berdugo, Iván Segura Carmona | 12 |
| 6.2 | Validación externa y test de DeLong | Luis Carmona Berdugo | 14 |

Tarea 6.1 – Comparación estadística: ranking y análisis exploratorio: se implementa el script que genera el ranking global de los modelos por su AUC medio y calcula una matriz exploratoria de p-valores por pares. Dado que solo se dispone de cinco folds dependientes, el test de Wilcoxon no se utilizará para afirmar significación confirmatoria; cualquier contraste por pares deberá incorporar una corrección por comparaciones múltiples y sus limitaciones deberán quedar documentadas. Es la tarea más costosa del sprint.

Tarea 6.2 – Validación externa y test de DeLong: se implementa la evaluación de los modelos congelados sobre la cohorte independiente de pacientes adultos y el test de DeLong para comparar las curvas ROC. Esta tarea constituye el examen de generalización del proyecto: sobre sus resultados se sustentan las conclusiones de la memoria. Genera las matrices de significación de la validación externa.

### 5.2.8 Sprint 7 – Laboratorio MLOps

El laboratorio MLOps es, junto con la infraestructura, el bloque de mayor carga del proyecto, con 66 horas en siete tareas. Integra el asistente conversacional basado en Groq y en el modelo `openai/gpt-oss-120b`, que permite al usuario configurar y lanzar experimentos en lenguaje natural sin escribir código: desde la integración de la API de Groq y el diseño del prompt hasta el lanzamiento de los experimentos desde la conversación. El sprint incorpora también la cola de trabajos que garantiza la ejecución asíncrona de diagnósticos, entrenamientos y validaciones externas, la internacionalización de la plataforma en cuatro idiomas y las vistas de resultados con el ranking, las matrices de significación y las curvas ROC. Se desarrolla en la última semana de mayo y la primera de junio y convierte el laboratorio en la puerta de entrada de los experimentos para el usuario investigador. Es, junto con el sprint de infraestructura, el más amplio del cronograma.

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

Tarea 7.2 – Diseño del prompt del asistente: se diseña el prompt de sistema que define al asistente como experto en MLOps médico. Incluye las reglas de extracción de los cinco parámetros del experimento —ruta del dataset, arquitecturas, épocas, lote y tasa de aprendizaje— y el formato JSON de salida. Es una tarea de diseño más que de código, y por eso su estimación es moderada.

Tarea 7.3 – Asistente conversacional del laboratorio: se implementa el endpoint de chat y la sala de conversación, con el historial de mensajes por sesión. El asistente interpreta la configuración devuelta por el modelo y la traduce al panel del experimento, para que el usuario pueda revisarla y confirmarla. Es la tarea más costosa del sprint.

Tarea 7.4 – Lanzamiento de experimentos desde el chat: se conecta la configuración detectada por el asistente con el lanzamiento del pipeline de entrenamiento, de modo que el experimento se encola y arranca sin escribir código.

Tarea 7.5 – Cola de trabajos y ejecución asíncrona: se implementa la cola de trabajos que gestiona los diagnósticos, los entrenamientos y las validaciones externas, con monitorización de estado y cancelación de las tareas pendientes.

Tarea 7.6 – Internacionalización de la plataforma: se incorpora el soporte multilingüe de la interfaz, los informes y el asistente en los cuatro idiomas de la plataforma, mediante atributos de traducción y diccionarios en JavaScript.

Tarea 7.7 – Vistas de resultados, rankings y curvas ROC: se construyen las vistas del laboratorio que muestran el ranking de modelos, las matrices de significación y las curvas ROC de la validación externa.

### 5.2.9 Sprint 8 – Documentación y cierre

El sprint final abandona el código para concentrarse en el benchmarking definitivo, la redacción de la memoria y de los manuales, las correcciones finales y la entrega. Con 67 horas en cuatro tareas, se desarrolla desde el 5 de junio hasta el 2 de septiembre de 2026, con una dedicación repartida entre la ejecución experimental, la documentación y el cierre. La redacción de la memoria es la tarea más extensa del sprint, mientras que las correcciones finales y la entrega se han separado en tareas específicas. El sprint culmina con la entrega del 2 de septiembre de 2026.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 8.1 | Benchmarking final con todas las arquitecturas | Luis Carmona Berdugo, Iván Segura Carmona, Marc Ríos Cadenas | 18 |
| 8.2 | Redacción de la memoria y manuales | Luis Carmona Berdugo | 30 |
| 8.3 | Reunión final y correcciones | Luis Carmona Berdugo, Aurelio López Fernández | 16 |
| 8.4 | Entrega final | Luis Carmona Berdugo | 3 |

Tarea 8.1 – Benchmarking final con todas las arquitecturas: se ejecuta la evaluación completa del banco de pruebas, consolidando las métricas de rendimiento, calibración y explicabilidad de las diecinueve arquitecturas mediante sus cinco pliegues de validación cruzada. La estimación de dieciocho horas constituye una previsión de ejecución, no una medición validada del rendimiento del hardware, y no incluye una reserva temporal para reentrenamientos completos. El asesor de deep learning y XAI y el asesor de imagen médica revisan la coherencia de los resultados y de los mapas de explicabilidad. Si una arquitectura no converge o el tiempo computacional impide completar el banco de pruebas, la contingencia viable dentro del calendario es reducir el alcance del benchmarking y documentar las arquitecturas o resultados excluidos; la sustitución y reejecución completa quedarían como trabajo posterior. Sus conclusiones alimentan directamente los capítulos de resultados y conclusiones de la memoria.

Tarea 8.2 – Redacción de la memoria y manuales: se redacta la memoria completa del Trabajo Fin de Grado, integrando el plan de proyecto, el análisis, el diseño, la implementación, las pruebas y las conclusiones, junto con el manual de usuario orientado a facultativos sin formación técnica. La redacción se realiza de forma incremental a lo largo de la fase de documentación, incorporando la revisión y las correcciones del tutor. Cada capítulo se elabora y se revisa por separado antes de su integración en el documento final. Es la tarea de mayor carga individual del proyecto, y su extensión justifica con holgura las treinta horas estimadas. El manual de usuario se redacta pensando en el profesional sanitario, con un lenguaje no técnico y capturas de los flujos principales.

Tarea 8.3 – Reunión final y correcciones: reunión con el tutor y periodo de corrección programados del 28 de agosto al 1 de septiembre. Esta tarea permite revisar el conjunto del trabajo, aplicar las correcciones detectadas, preparar la defensa y dejar la versión final lista antes de la entrega.

Tarea 8.4 – Entrega final: depósito de la memoria y de los entregables del proyecto el 2 de septiembre de 2026. Esta tarea constituye el cierre administrativo posterior a la revisión y corrección final.

## 5.3 Recursos y costes del proyecto

Este apartado detalla la asignación de recursos del proyecto, abarcando todo lo necesario para ejecutar las tareas descritas anteriormente. Se establecen dos categorías fundamentales: los recursos de trabajo, centrados en el capital humano, y los recursos materiales, que engloban la infraestructura y el equipamiento tecnológico.

Microsoft Project centraliza la administración del proyecto. Los recursos ocasionales, como el tutor y los asesores, reciben un horario fijo; esto impide que el software reasigne automáticamente su esfuerzo ante variaciones en la duración de las tareas. Todas las asignaciones se han auditado manualmente para que la carga de los recursos laborables sea coherente con la dedicación real de cada fase del proyecto.

**Recursos de trabajo:**

- **Luis Carmona Berdugo**: asume la carga técnica integral del proyecto. Acumula 455,14 horas distribuidas a lo largo de todos los sprints. Con una tarifa estándar de 20 €/h, su esfuerzo se cuantifica en 9.102,80 €.
- **Aurelio López Fernández (tutor)**: interviene estratégicamente en los hitos de apertura (tarea 0.1) y de clausura y correcciones (tarea 8.3). Dedica 9,5 horas de supervisión a 50 €/h, sumando un total de 475,00 €.
- **Iván Segura Carmona (asesor de Deep Learning y XAI)**: supervisa el núcleo algorítmico. Valida las implementaciones de explicabilidad, los pipelines CNN y Transformer, la comparación estadística y el benchmarking definitivo. Acumula 5,96 horas a 50 €/h, con un total de 298,00 €.
- **Marc Ríos Cadenas (asesor de Imagen Médica)**: aporta el rigor clínico. Participa en la revisión de la coherencia de los mapas de explicabilidad y en la validación del benchmarking. Dedica 1,9 horas a 50 €/h, sumando 95,00 €.
- **Vicente de Vides Rodríguez (consultor de persistencia y bases de datos)**: aporta su experiencia estructural en el diseño y la optimización de la persistencia de datos. Participa en la tarea 1.1 con 1,5 horas a 50 €/h, con un total de 75,00 €.

El coste total de los recursos de trabajo asciende, por tanto, a aproximadamente 10.045,80 €.

**Recursos materiales:**

- **Equipo de desarrollo**: se utiliza un equipo local con GPU NVIDIA compatible con CUDA, disponible para el desarrollo. El plan no especifica el modelo de GPU ni su memoria VRAM, por lo que la viabilidad de las arquitecturas con mayor resolución o capacidad no puede justificarse únicamente desde este apartado. Al tratarse de infraestructura ya disponible, no se imputa una amortización adicional al TFG.
- **Licencias de software**: coste nulo. La plataforma descansa enteramente sobre tecnologías de código abierto (Python, TensorFlow, FastAPI, MySQL), eliminando cualquier gasto de licenciamiento.
- **Servicios cloud**: no se presupuesta ningún servicio cloud en el plan base. La nube aparece únicamente como contingencia ante un fallo del equipo local, pero no existe una reserva económica asignada; si fuera necesario activarla, habría que aprobar un coste adicional o reducir el alcance del benchmarking y documentar la decisión.
- **Electricidad y API de Groq**: no se dispone de una medición o factura imputable exclusivamente al proyecto, por lo que ambos conceptos quedan fuera del presupuesto cuantificado. El consumo energético se reconoce como impacto operativo y el uso de Groq queda sujeto al plan y a las cuotas vigentes del servicio.

El coste económico documentado del proyecto asciende a **10.045,80 €**, correspondiente a los recursos humanos presupuestados. Esta cifra no debe interpretarse como un coste completo de explotación: excluye la amortización del equipo ya disponible, la electricidad, una eventual infraestructura cloud y cualquier consumo facturado de la API de Groq.

## 5.4 Reparto de responsabilidades

Este apartado recoge la distribución de responsabilidades sobre las tareas definidas en el apartado 5.2. Para cada tarea se identifica qué persona asume la titularidad, qué interesados intervienen de forma puntual y en qué proporción. El reparto porcentual de cada responsable sobre cada tarea —recogido en las tablas del apartado 5.2— constituye la base sobre la que se calculan las horas y los costes del apartado 5.3, y se apoya en los roles definidos en la matriz RACI del capítulo de organización. La lógica del reparto es sencilla: el alumno desarrollador concentra la práctica totalidad de la carga de trabajo, mientras que el resto de los interesados participa de forma puntual y consultiva en los hitos donde su conocimiento especializado resulta indispensable.

La responsabilidad absoluta sobre la ejecución del proyecto recae sobre Luis Carmona Berdugo. El alumno asume en solitario todo el peso técnico y documental a lo largo de los nueve sprints, acumulando 455,14 horas de trabajo, lo que representa prácticamente la totalidad del esfuerzo planificado. Su figura absorbe íntegramente los roles de analista, diseñador, desarrollador backend y frontend, ingeniero de deep learning, tester y documentador: analiza los requisitos, diseña la arquitectura, implementa tanto el backend como la interfaz, construye los pipelines de entrenamiento y los módulos XAI, ejecuta el benchmarking y redacta toda la documentación del proyecto. Al tratarse de un Trabajo Fin de Grado, el desarrollo carece de un reparto transversal de tareas entre distintos perfiles profesionales, y es precisamente esta concentración la que justifica que el alumno asuma prácticamente el cien por cien de las horas en la mayoría de las tareas. En las tareas en las que intervienen los asesores, su participación sigue siendo mayoritaria, con porcentajes que oscilan entre el 50% de las reuniones y el 97% de las tareas de entrenamiento.

No obstante, la profunda naturaleza multidisciplinar del sistema exige el apoyo puntual y consultivo de varios interesados. Estas figuras aportan su conocimiento especializado y auditan el proceso únicamente en aquellos hitos donde su validación resulta indispensable para garantizar el rigor del proyecto. A continuación se describe de forma pormenorizada la participación exacta de cada uno de ellos.

Aurelio López Fernández asume la figura central de tutor académico y científico del proyecto. Su participación remunerada se concentra en dos hitos concretos del cronograma: la tarea 0.1, correspondiente a la reunión inicial, y la tarea 8.3, correspondiente a la reunión final y al periodo de correcciones. En ambas comparte la dedicación al cincuenta por ciento con el alumno, lo que supone un total de 9,5 horas de supervisión y un coste de 475 €. El seguimiento del resto del ciclo se realiza mediante comunicación y revisiones puntuales dentro de la dedicación académica del proyecto, pero no se computa como dieciocho reuniones formales ni como horas adicionales en el presupuesto.

Iván Segura Carmona actúa como asesor experto en aprendizaje profundo e inteligencia artificial explicable. Su participación, de naturaleza estrictamente consultiva, se distribuye a lo largo de los sprints de implementación técnica, donde valida el trabajo del alumno en los puntos más sensibles del proceso experimental. En el Sprint 3 revisa la implementación de las técnicas XAI (tareas 3.1 y 3.3, con una dedicación del 10% y del 8% respectivamente); en el Sprint 4 inspecciona el pipeline de entrenamiento convolucional (tarea 4.1, 3%); en el Sprint 5 valida el script de entrenamiento de los Transformers y el cálculo de las métricas cuantitativas (tareas 5.1 y 5.3, con un 3% y un 8%) y revisa los resultados junto al alumno (tarea 5.6, 25%); en el Sprint 6 revisa la comparación estadística (tarea 6.1, 8%); y en el Sprint 8 certifica los resultados del benchmarking final (tarea 8.1, 5%). Su dedicación total asciende a 5,96 horas, con un coste de 298 €.

Marc Ríos Cadenas interviene como asesor especialista en imagen médica. Su participación mantiene un perfil consultivo y se concentra en dos hitos que exigen criterio clínico: la revisión de la coherencia de los mapas de explicabilidad en la tarea 3.6, donde comprueba que los mapas apuntan a las regiones pulmonares relevantes y no a artefactos, y la validación de los resultados del benchmarking final en la tarea 8.1, donde certifica la coherencia diagnóstica de las explicaciones frente al criterio médico humano. Su dedicación, del 25% en la tarea 3.6 y del 5% en la tarea 8.1, asciende a 1,9 horas y a un coste de 95 €.

Vicente de Vides Rodríguez actúa como consultor de persistencia y bases de datos. Su intervención es puntual y estrictamente consultiva, concentrándose en la tarea 1.1, correspondiente al diseño del modelo de datos en MySQL. En ella aporta su experiencia estructural y verifica que el modelo de persistencia de la información resulta coherente con las exigencias de almacenamiento del sistema, sin asumir en ningún caso la implementación, que corresponde al alumno. Su dedicación del 15% sobre dicha tarea supone 1,5 horas y un coste de 75 €.

El resto de las partes interesadas identificadas en el capítulo de organización, como el asesor de ingeniería del software y metodología, participan únicamente a través de la matriz RACI, sin asumir tareas concretas ni horas asignadas en el cronograma del proyecto. En conjunto, el reparto de responsabilidades refleja una realidad propia de un trabajo académico unipersonal: una carga técnica casi íntegramente asumida por el alumno, complementada por intervenciones puntuales y de alto valor de los asesores, cuyos costes se consolidan en el apartado 5.3.
