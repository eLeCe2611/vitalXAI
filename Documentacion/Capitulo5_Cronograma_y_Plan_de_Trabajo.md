# Capítulo 5: Cronograma y Plan de Trabajo

## 5.1 Alcance y objetivos del programa de trabajo

Este proyecto se centra en el desarrollo de una plataforma web MLOps que integre inteligencia artificial explicable para el diagnóstico asistido de neumonía mediante radiografías de tórax. El sistema permitirá a los facultativos cargar radiografías, obtener diagnósticos con distintas arquitecturas de deep learning, visualizar mapas de calor interpretativos y descargar informes PDF, así como acceder a un laboratorio de entrenamiento automatizado que ejecuta pipelines completos de validación cruzada, análisis de explicabilidad y validación externa. Todo ello estará securizado bajo un sistema de autenticación para garantizar la privacidad de los datos de los pacientes y los historiales de los profesionales sanitarios.

El proyecto se ha desarrollado siguiendo una metodología ágil Scrum, estructurando el trabajo en Sprints de duración fija de dos semanas. Dentro de la metodología Scrum, la duración de cada uno de los Sprints es importante ya que debe ser fija, adaptando la cantidad de trabajo en cada iteración y no la duración de esta. Cada Sprint debe producir un incremento de producto potencialmente entregable que integra diseño, implementación y pruebas de forma simultánea, de forma que no se constituyan fases aisladas y secuenciales. Las pruebas se realizan de forma continua e incremental a lo largo de todo el proyecto, incluyendo las pruebas de seguridad en los mismos Sprints en que se desarrollan los componentes afectados, validando cada incremento antes de avanzar al siguiente.

La premisa de planificación que tiene el calendario de este proyecto es que se establece una dedicación media de seis horas diarias, lo que permite relacionar con coherencia matemática las horas estimadas por cada una de las tareas con los días de duración que aparecen en el Diagrama de Gantt. Con esta dedicación, una tarea de diez horas equivale aproximadamente a dos días en el diagrama de Gantt.

## 5.2 Plan de tareas

La planificación de tareas se estructura en torno a nueve Sprints, establecidos por la metodología Scrum implementada. Cada Sprint tiene una duración de dos semanas y constituye una unidad de trabajo iterativa con un propósito definido y un incremento verificable del producto funcional. Los Sprints son secuenciales de manera rigurosa, lo que significa que el Sprint N+1 no podrá empezar hasta que el anterior haya concluido su revisión y retrospectiva.

El camino crítico discurre por las tareas que tienen mayor carga técnica y menor paralelizabilidad: implementación del pipeline de entrenamiento CNN (Sprint 4) e implementación del pipeline Transformer (Sprint 5), que deben completarse antes de poder realizar el benchmarking final. Estas tareas no pueden comenzar hasta que la anterior haya concluido y concentran el mayor riesgo de retraso del proyecto.

### 5.2.1 Sprint 0 – Planificación del proyecto

Este Sprint tiene como objetivo establecer todas las bases organizativas, técnicas y documentales del proyecto antes del inicio del desarrollo. Es el único Sprint en el que no hay código ni artefactos de software, sino únicamente documentación de gestión y planificación.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 0.1 | Reunión inicial | Luis Carmona Berdugo, Aurelio López Fernández | 3 |
| 0.2 | Documentación de gestión | Luis Carmona Berdugo | 25 |
| 0.3 | Identificación de recursos necesarios | Luis Carmona Berdugo | 4 |
| 0.4 | Desarrollo del cronograma de planificación | Luis Carmona Berdugo | 6 |

**Tarea 0.1 – Reunión Inicial**: Reunión inicial del proyecto que se realiza entre el tutor y el alumno. En esta reunión se definen los objetivos generales del TFG, el alcance del sistema, las tecnologías a utilizar (FastAPI, TensorFlow, MySQL, Groq), la metodología de trabajo que se va a utilizar y la planificación inicial del proyecto.

**Tarea 0.2 – Documentación de Gestión**: En esta tarea se redacta el Plan de Proyecto en el que se incluye la definición de los objetivos, la organización del proyecto, la metodología, el plan de tareas y la evaluación de riesgos. Las veinticinco horas que se utilizan se justifican por la extensión y profundidad del documento, ya que debe cubrir todos los aspectos propios de un TFG.

**Tarea 0.3 – Identificación de recursos necesarios**: La identificación y evaluación de las herramientas, librerías, frameworks y entornos necesarios a lo largo del proyecto se realizan dentro de esta tarea. Se evalúan las versiones de TensorFlow, Keras, FastAPI, MySQL y las dependencias de los modelos Transformer de HuggingFace.

**Tarea 0.4 – Desarrollo del cronograma de planificación**: Elaboración del Diagrama de Gantt y la planificación por Sprints, incluyendo la definición de dependencias entre cada una de las tareas, la asignación de recursos y el cálculo del camino crítico.

### 5.2.2 Sprint 1 – Infraestructura base: API, base de datos y autenticación

El primer Sprint de desarrollo produce el primer incremento funcional del sistema: un backend FastAPI operativo con una base de datos MySQL, autenticación de usuarios y capacidad de servir páginas web estáticas.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 1.1 | Análisis y diseño del sistema | Luis Carmona Berdugo | 10 |
| 1.2 | Diseño y construcción de la base de datos | Luis Carmona Berdugo, Domingo S. Rodríguez Baena | 12 |
| 1.3 | Implementación de la API base y autenticación | Luis Carmona Berdugo | 15 |
| 1.4 | Interfaz web de login y registro | Luis Carmona Berdugo | 10 |
| 1.5 | Pruebas de seguridad (autenticación y BBDD) | Luis Carmona Berdugo | 8 |

**Tarea 1.1 – Análisis y diseño del sistema**: Se definen dentro de esta tarea el alcance del sistema, los requisitos funcionales y no funcionales principales, el modelo de dominio y la arquitectura de alto nivel. El análisis se limita a lo necesario para el Sprint en curso, aplicando el principio ágil de diseño emergente.

**Tarea 1.2 – Diseño y construcción de la base de datos**: Dentro de esta tarea se realiza el diseño del diagrama Entidad-Relación de la base de datos, la traducción al modelo relacional y la implementación del esquema físico en MySQL. Se diseñan las tablas para usuarios, consultas de diagnóstico e historiales de entrenamiento. La participación de Domingo S. Rodríguez Baena como asesor se concentra en esta tarea con una hora de revisión del diseño E/R y una hora de revisión del esquema físico resultante.

**Tarea 1.3 – Implementación de la API base y autenticación**: Desarrollo de los endpoints de registro, login, dashboard y cierre de sesión, así como los endpoints base para la gestión de consultas y el historial. Se utiliza Jinja2 para el renderizado de plantillas HTML en el servidor.

**Tarea 1.4 – Interfaz web de login y registro**: Implementación de las pantallas de login, registro y dashboard básico. Este incremento visual permite verificar de manera integral el flujo completo de autenticación.

**Tarea 1.5 – Pruebas de seguridad (autenticación y BBDD)**: Validación de la autenticación y autorización, pruebas de inyección SQL sobre los endpoints implementados y verificación de que los datos sensibles no se exponen en las respuestas de la API.

### 5.2.3 Sprint 2 – Motor de inferencia y frontend clínico

Este Sprint implementa el núcleo del diagnóstico clínico: la carga de modelos preentrenados, el endpoint de predicción y la interfaz web que permite a los facultativos cargar radiografías y visualizar resultados.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 2.1 | Implementación del motor de carga de modelos | Luis Carmona Berdugo | 15 |
| 2.2 | Endpoint de predicción con CNN | Luis Carmona Berdugo | 12 |
| 2.3 | Frontend de diagnóstico: subida de imagen y resultados | Luis Carmona Berdugo | 15 |
| 2.4 | Generación de informes PDF | Luis Carmona Berdugo | 10 |
| 2.5 | Pruebas de integración del flujo de diagnóstico | Luis Carmona Berdugo | 8 |

**Tarea 2.1 – Implementación del motor de carga de modelos**: Desarrollo del módulo `ml_engine.py` que gestiona la carga en memoria de los modelos CNN preentrenados y su caché. Se implementa la lógica de diferenciación entre arquitecturas CNN (carga con `load_model` de Keras) y Transformer (carga mediante `TFAutoModelForImageClassification` de HuggingFace).

**Tarea 2.2 – Endpoint de predicción con CNN**: Implementación del endpoint `/predict` que recibe una imagen y el nombre del modelo, ejecuta la inferencia y devuelve la etiqueta diagnóstica y el nivel de confianza. Se implementa el preprocesamiento de imagen con OpenCV, adaptando el tamaño según la arquitectura seleccionada.

**Tarea 2.3 – Frontend de diagnóstico**: Implementación de la pantalla de diagnóstico en el dashboard clínico, con un formulario de subida de imagen, selector de modelo y visualización de resultados. La interfaz se diseña siguiendo criterios de simplicidad para usuarios no técnicos.

**Tarea 2.4 – Generación de informes PDF**: Desarrollo del módulo `pdf_generator.py` que genera un informe PDF con la radiografía original, el diagnóstico, el nivel de confianza y el modelo utilizado, empleando la librería FPDF.

**Tarea 2.5 – Pruebas de integración**: Verificación del flujo completo de diagnóstico: subida de imagen, inferencia, almacenamiento en base de datos y generación del informe PDF.

### 5.2.4 Sprint 3 – Módulo de explicabilidad XAI

Este Sprint añade las capacidades de inteligencia artificial explicable al sistema, generando mapas de calor visuales que permiten a los clínicos comprender las regiones de la radiografía que han influido en cada predicción.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 3.1 | Implementación de Saliency Maps | Luis Carmona Berdugo, Iván Segura-Carmona | 12 |
| 3.2 | Implementación de SmoothGrad | Luis Carmona Berdugo | 10 |
| 3.3 | Implementación de Grad-CAM y Attention Maps | Luis Carmona Berdugo, Iván Segura-Carmona | 14 |
| 3.4 | Integración XAI en el endpoint de predicción | Luis Carmona Berdugo | 8 |
| 3.5 | Frontend: visualización de mapas de calor | Luis Carmona Berdugo | 10 |

**Tarea 3.1 – Implementación de Saliency Maps**: Desarrollo de la función que calcula el mapa de prominencia mediante el gradiente de la clase predicha respecto a la imagen de entrada, utilizando `tf.GradientTape`.

**Tarea 3.2 – Implementación de SmoothGrad**: Desarrollo de la variante que promedia múltiples mapas de saliencia generados a partir de versiones con ruido gaussiano de la imagen original, mejorando la estabilidad de las explicaciones.

**Tarea 3.3 – Implementación de Grad-CAM y Attention Maps**: Para arquitecturas CNN, se implementa Grad-CAM localizando la última capa convolucional y calculando los pesos de importancia. Para arquitecturas Transformer, se implementa la extracción de los mapas de atención de la última capa del modelo, promediando entre cabezas de atención. La revisión técnica del asesor Iván Segura-Carmona (una hora) valida la correcta implementación de ambas técnicas.

**Tarea 3.4 – Integración XAI en el endpoint de predicción**: Modificación del endpoint `/predict` para que, además de la predicción, genere y almacene los tres mapas de explicabilidad, devolviendo las rutas de las imágenes generadas.

**Tarea 3.5 – Frontend: visualización de mapas de calor**: Implementación de la visualización en mosaico 1x4 en la interfaz clínica, mostrando la radiografía original junto con los tres mapas XAI generados.

### 5.2.5 Sprint 4 – Pipeline de entrenamiento CNN

Este Sprint implementa el primer pipeline de entrenamiento automatizado, permitiendo entrenar arquitecturas convolucionales con validación cruzada estratificada de cinco pliegues.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 4.1 | Desarrollo del script de entrenamiento CNN | Luis Carmona Berdugo, Iván Segura-Carmona | 20 |
| 4.2 | Integración del entrenamiento en el backend | Luis Carmona Berdugo | 10 |
| 4.3 | Frontend: panel de monitorización de entrenamiento | Luis Carmona Berdugo | 12 |
| 4.4 | Pruebas de corrección del pipeline CNN | Luis Carmona Berdugo | 10 |

**Tarea 4.1 – Desarrollo del script de entrenamiento CNN**: Implementación del script `1_train_kfold.py` que entrena las arquitecturas convolucionales utilizando validación cruzada estratificada de cinco pliegues con balanceo de clases. El script acepta variables de entorno para la configuración del experimento y almacena los resultados en formato CSV. Las veinte horas incluyen la implementación del pipeline de datos con TensorFlow Dataset, la construcción dinámica de cada arquitectura y el guardado de los pesos de cada pliegue. La revisión del asesor Iván Segura-Carmona (una hora) valida la correcta implementación del pipeline de entrenamiento.

**Tarea 4.2 – Integración del entrenamiento en el backend**: Desarrollo del endpoint `/api/train/start` que recibe la configuración del experimento y lanza la ejecución del script de entrenamiento como un proceso en segundo plano, almacenando el progreso y los resultados.

**Tarea 4.3 – Frontend: panel de monitorización**: Implementación de la interfaz de monitorización del entrenamiento que muestra el progreso en tiempo real, los logs de ejecución y permite la cancelación de experimentos.

**Tarea 4.4 – Pruebas de corrección**: Verificación de que los resultados de entrenamiento son reproducibles y consistentes, ejecutando el pipeline completo con un conjunto de datos de prueba y comprobando que las métricas se almacenan correctamente.

### 5.2.6 Sprint 5 – Pipeline Transformer y XAI

Este Sprint extiende el marco de entrenamiento a las arquitecturas Transformer e implementa los módulos de análisis XAI cualitativo y cuantitativo que se ejecutan automáticamente tras cada entrenamiento.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 5.1 | Desarrollo del script de entrenamiento Transformer | Luis Carmona Berdugo, Iván Segura-Carmona | 18 |
| 5.2 | Desarrollo del script de XAI cualitativo | Luis Carmona Berdugo | 12 |
| 5.3 | Desarrollo del script de XAI cuantitativo | Luis Carmona Berdugo, Iván Segura-Carmona | 14 |
| 5.4 | Orquestación automática post-entrenamiento | Luis Carmona Berdugo | 8 |
| 5.5 | Pruebas de integración del pipeline completo | Luis Carmona Berdugo | 10 |

**Tarea 5.1 – Desarrollo del script de entrenamiento Transformer**: Implementación del script `2_train_transformer_kfold.py` que entrena las arquitecturas DeiT, Swin-Base y ViT-384 utilizando HuggingFace Transformers con validación cruzada de cinco pliegues.

**Tarea 5.2 – Desarrollo del script de XAI cualitativo**: Implementación del script `6_xai_qualitative.py` que genera mapas de calor visuales (Saliency Maps, SmoothGrad, Grad-CAM o Attention Maps) para cada modelo entrenado, creando un conjunto de imágenes de ejemplo.

**Tarea 5.3 – Desarrollo del script de XAI cuantitativo**: Implementación del script `7_xai_quantitative.py` que calcula las métricas numéricas de fidelidad de las explicaciones: Deletion AUC, Insertion AUC, Sparsity, Entropy y Stability SSIM. Adicionalmente, se incorpora la métrica Expected Calibration Error (ECE) como mejora respecto al estudio de referencia.

**Tarea 5.4 – Orquestación automática**: Desarrollo del sistema de llamadas automáticas a los scripts XAI tras la finalización de cada entrenamiento, garantizando que ningún modelo quede sin su correspondiente evaluación de explicabilidad.

**Tarea 5.5 – Pruebas de integración**: Verificación del flujo completo de entrenamiento Transformer seguido de la generación automática de XAI cualitativo y cuantitativo.

### 5.2.7 Sprint 6 – Validación externa y análisis estadístico

Este Sprint implementa los mecanismos de validación externa y los tests estadísticos que permiten determinar la significación de las diferencias entre modelos.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 6.1 | Desarrollo del script de evaluación estadística | Luis Carmona Berdugo, Iván Segura-Carmona | 14 |
| 6.2 | Desarrollo del script de validación externa | Luis Carmona Berdugo | 12 |
| 6.3 | Desarrollo del test de DeLong | Luis Carmona Berdugo | 10 |
| 6.4 | Integración de validación externa en el backend | Luis Carmona Berdugo | 8 |
| 6.5 | Frontend: visualización de rankings y comparativas | Luis Carmona Berdugo | 12 |

**Tarea 6.1 – Desarrollo del script de evaluación estadística**: Implementación del script `3_evaluate_statistics.py` que genera el ranking global de modelos basado en la media y desviación típica del AUC de los cinco pliegues, y aplica el test de Wilcoxon para determinar la significación estadística de las diferencias entre todos los pares de modelos, generando una matriz de calor de p-valores.

**Tarea 6.2 – Desarrollo del script de validación externa**: Implementación del script `4_external_validation.py` que evalúa todos los modelos entrenados sobre un conjunto de datos independiente (COVID-19 Radiography Database) con quinientas imágenes sanas y quinientas con neumonía. Los modelos se cargan congelados, sin reaprendizaje.

**Tarea 6.3 – Desarrollo del test de DeLong**: Implementación del script `5_evaluate_delong.py` que aplica el test de DeLong para la comparación pareada de curvas ROC entre modelos sobre los resultados de la validación externa, generando una matriz de calor de significación.

**Tarea 6.4 – Integración de validación externa**: Desarrollo de los endpoints para lanzar la validación externa desde el laboratorio MLOps y consultar los resultados almacenados.

**Tarea 6.5 – Frontend de rankings**: Implementación de las vistas de ranking de modelos, matriz de Wilcoxon, curvas ROC de validación externa y matriz de DeLong en el frontend del laboratorio.

### 5.2.8 Sprint 7 – Laboratorio MLOps y chatbot conversacional

Este Sprint integra el asistente conversacional basado en Groq (Llama 3) que guía al usuario en la configuración de experimentos de entrenamiento sin necesidad de escribir código.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 7.1 | Integración de la API de Groq | Luis Carmona Berdugo | 10 |
| 7.2 | Desarrollo del sistema de prompt engineering | Luis Carmona Berdugo | 12 |
| 7.3 | Implementación del chatbot conversacional | Luis Carmona Berdugo | 14 |
| 7.4 | Integración chatbot- entrenamiento | Luis Carmona Berdugo | 10 |
| 7.5 | Frontend: sala de chat y panel de control MLOps | Luis Carmona Berdugo | 14 |

**Tarea 7.1 – Integración de la API de Groq**: Configuración del cliente Groq y establecimiento de la conexión con el modelo Llama 3.3-70B para el asistente conversacional.

**Tarea 7.2 – Desarrollo del sistema de prompt engineering**: Diseño e implementación del prompt de sistema que define el comportamiento del asistente como experto en MLOps médico, estableciendo las reglas de extracción de parámetros y el formato de salida JSON para la ejecución de entrenamientos.

**Tarea 7.3 – Implementación del chatbot**: Desarrollo del endpoint `/api/chat` que gestiona las sesiones conversacionales con historial de mensajes, permitiendo al usuario interactuar de manera natural con el sistema.

**Tarea 7.4 – Integración chatbot-entrenamiento**: Implementación del orquestador que procesa la salida JSON del chatbot y lanza el pipeline completo de entrenamiento con los parámetros especificados por el usuario.

**Tarea 7.5 – Frontend de laboratorio MLOps**: Implementación de la interfaz del laboratorio con sala de chat conversacional, panel de configuración de experimentos, monitorización de progreso y visualización de resultados históricos.

### 5.2.9 Sprint 8 – Benchmarking final, documentación y cierre

El Sprint final está dedicado al benchmarking completo del sistema, la elaboración de la documentación del usuario y la entrega formal del TFG.

| Código | Nombre | Responsable(s) | Estimación (h) |
|---|---|---|---|
| 8.1 | Benchmarking final de rendimiento | Luis Carmona Berdugo, Iván Segura-Carmona | 20 |
| 8.2 | Elaboración de la memoria del TFG | Luis Carmona Berdugo | 30 |
| 8.3 | Redacción de manuales | Luis Carmona Berdugo | 15 |
| 8.4 | Reunión final | Luis Carmona Berdugo, Aurelio López Fernández | 2 |
| 8.5 | Cierre del proyecto | Luis Carmona Berdugo | 5 |

**Tarea 8.1 – Benchmarking final de rendimiento**: Ejecución completa del pipeline de benchmarking con todas las arquitecturas implementadas, midiendo y comparando las métricas de rendimiento predictivo (Accuracy, Precision, Recall, F1, AUC), las métricas de calibración (ECE) y las métricas de explicabilidad (Deletion AUC, Insertion AUC, Sparsity, Entropy, Stability SSIM). Se analizan y documentan los resultados, identificando las arquitecturas con mejor rendimiento global.

**Tarea 8.2 – Elaboración de la memoria del TFG**: Redacción completa de la memoria del Trabajo Fin de Grado, integrando todos los capítulos elaborados a lo largo de los Sprints anteriores.

**Tarea 8.3 – Redacción de manuales**: Elaboración del manual de usuario, orientado a facultativos sin formación técnica, y del manual de instalación y configuración del sistema para entornos clínicos.

**Tarea 8.4 – Reunión final**: Última reunión entre el alumno y el tutor, en la que se revisa el TFG en su conjunto, el tutor valida la entrega y se acuerdan los últimos ajustes antes de la entrega final.

**Tarea 8.5 – Cierre del proyecto**: Preparación de la presentación final, empaquetado y entrega del proyecto (código fuente, documentación y manuales) a través del sistema habilitado para ello.

## 5.3 Asignación de recursos

En este apartado se recoge la asignación de recursos del proyecto, entendiendo como recurso todo aquello necesario para llevar a cabo las tareas definidas en el punto anterior. Se distinguen dos tipos de recursos: los recursos de trabajo (personas) y los recursos materiales (infraestructura y equipamiento).

**Recursos de trabajo:**

- Luis Carmona Berdugo acumula un total de 320 horas de trabajo distribuidas a lo largo de todos los Sprints del proyecto, con una tasa estándar de 20,00 €/hora, lo que hace un total de 6.400 €.
- Aurelio López Fernández (tutor) interviene en la Reunión Inicial (Sprint 0) y la Reunión Final (Sprint 8), acumulando un total de 5 horas a una tasa de 50 €/h, con un total de 250 €.
- Domingo S. Rodríguez Baena (asesor BBDD) participa en el diseño y construcción de la base de datos (Sprint 1) con un total de 2 horas a 50 €/h y un coste de 100 €.
- Iván Segura-Carmona (asesor Deep Learning y XAI) interviene en la revisión de las implementaciones de XAI, los pipelines de entrenamiento CNN y Transformer, y el benchmarking final, acumulando 8 horas a 50 €/h que implica un coste total de 400 €.
- Marc Ríos-Cadenas (asesor Imagen Médica) participa en el análisis de requisitos (Sprint 1) y en la revisión de resultados (Sprint 8), con 2 horas asignadas y un coste total de 100 €.

**Recursos Materiales:**

- Equipo de desarrollo: portátil con GPU NVIDIA compatible con CUDA, adquirido para el desarrollo del proyecto con un coste de 1.800 €. Aplicando una amortización con una vida útil de 4 años y una duración del proyecto de 5 meses, el coste imputable al TFG asciende a 187,50 €.
- Licencias de software: todo el software utilizado es de código abierto y gratuito (Python, TensorFlow, FastAPI, MySQL), por lo que no genera costes de licenciamiento.
- Servicios cloud: no se requieren instancias cloud adicionales, ya que el entrenamiento se realiza íntegramente en el equipo local con GPU.

## 5.4 Asignación de tareas

En este apartado se describe la distribución de responsabilidades sobre las tareas definidas en el apartado 5.2, identificando qué persona es responsable de cada una de ellas y en qué medida participan el resto de los interesados definidos en el apartado 3.

La responsabilidad completa de la ejecución del proyecto recae sobre Luis Carmona Berdugo, que asume en solitario todo el peso técnico y documental a lo largo de cada uno de los Sprints, abarcando los roles de analista, diseñador, desarrollador backend y frontend, ingeniero de deep learning y tester. Al tratarse de un Trabajo Fin de Grado, no existe reparto de tareas entre distintos perfiles. No obstante, la naturaleza multidisciplinar del proyecto hace que varios interesados participen de manera puntual y consultiva en determinadas tareas, aportando su conocimiento especializado.

Aurelio López Fernández actúa como tutor académico y científico del proyecto. Su participación es transversal a lo largo de todos los Sprints. Su implicación no está limitada únicamente a la orientación de las decisiones técnicas y metodológicas más relevantes, sino que participa de manera activa en la tarea 0.1 (Reunión Inicial) y la tarea 8.4 (Reunión Final). Antes del cierre de cada Sprint, revisa y valida los artefactos producidos antes de dar el visto bueno para avanzar al siguiente.

Domingo S. Rodríguez Baena está involucrado como consultor en diseño y administración de bases de datos. Su intervención es puntual y se enfoca en el Sprint 1, apoyando la tarea 1.2 (Diseño y construcción de la base de datos) para verificar que el modelo de persistencia sea coherente con las exigencias del sistema.

Iván Segura-Carmona es el asesor especializado en deep learning y XAI. Su participación es consultiva y se distribuye a lo largo de los Sprints de implementación técnica: revisión de las implementaciones de XAI en el Sprint 3, revisión del pipeline de entrenamiento CNN en el Sprint 4, revisión del pipeline Transformer y XAI cuantitativo en el Sprint 5, y validación de los resultados del benchmarking en el Sprint 8.

Marc Ríos-Cadenas participa como asesor de imagen médica. Su participación es consultiva y se concentra en la revisión de requisitos durante el Sprint 1 y en la validación de los resultados del benchmarking durante el Sprint 8, verificando que los mapas de calor generados tienen coherencia clínica.

El grupo de investigación Synergia y los facultativos e investigadores clínicos están identificados como usuarios finales del sistema, por lo que no participan de manera activa en ninguna de las tareas. Sus necesidades y requerimientos son trasladados a través de Marc Ríos-Cadenas y se toman en cuenta como criterios de éxito del sistema, condicionando de manera indirecta la definición de los requisitos y los criterios de aceptación.
