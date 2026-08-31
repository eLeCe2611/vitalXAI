# Capítulo 6: Identificación y Mitigación de Riesgos

La gestión de riesgos forma parte de la planificación del proyecto. Su importancia aumenta cuando el sistema combina aprendizaje profundo, inteligencia artificial explicable y varias arquitecturas algorítmicas. En este capítulo se considera riesgo cualquier evento que pueda afectar negativamente al alcance, al calendario, a la calidad técnica o al coste del proyecto. El objetivo es identificar estos eventos, valorar su probabilidad e impacto y definir una respuesta ordenada para reducir sus consecuencias.

Para cada riesgo se definen dos respuestas. El plan de mitigación reúne las medidas preventivas que se aplican antes de que ocurra el evento, mientras que el plan de contingencia recoge las acciones que se adoptan cuando el riesgo ya se ha materializado. Ambos planes buscan limitar el impacto sobre el desarrollo del proyecto.

## 6.1 Escala de valoración de riesgos

Antes de presentar el catálogo de riesgos se establece la escala utilizada para valorar su probabilidad, severidad y prioridad.

La probabilidad estima la posibilidad de que el evento ocurra durante el ciclo de vida del proyecto. Se divide en tres niveles:

- **Baja**: El evento es poco probable o está limitado por medidas de control conocidas.
- **Media**: El evento puede producirse bajo determinadas condiciones del proyecto.
- **Alta**: El evento es frecuente o resulta difícil de controlar en proyectos de esta naturaleza.

La severidad cuantifica el impacto sobre el proyecto si el riesgo se materializa. Se establecen cuatro niveles:

- **Baja**: El impacto puede corregirse sin cambios relevantes en el alcance o el calendario.
- **Media**: El impacto afecta al tiempo, al coste o a la calidad y requiere medidas correctoras.
- **Alta**: El impacto compromete una parte importante del proyecto y puede exigir cambios de alcance o calendario.
- **Muy Alta**: El impacto puede impedir la finalización del proyecto o invalidar una parte esencial de sus resultados.

La prioridad se obtiene combinando la probabilidad y la severidad. La matriz siguiente muestra el resultado de esa combinación:

| Probabilidad \ Severidad | Baja | Media | Alta | Muy Alta |
|---|---|---|---|---|
| Baja | Baja | Baja | Media | Alta |
| Media | Baja | Media | Alta | Alta |
| Alta | Media | Alta | Alta | Muy Alta |

*Tabla 1 - Matriz de Prioridad*

## 6.2 Catálogo de riesgos identificados

A continuación, se presentan los riesgos identificados para este proyecto, clasificados por su origen, evaluados según su probabilidad y la severidad de su impacto, y priorizados mediante la matriz del apartado anterior. Se han identificado nueve riesgos relacionados con la gestión, la infraestructura y la implementación tecnológica, entre ellos la incompatibilidad de librerías, la disponibilidad de los conjuntos de datos médicos y el rendimiento de los modelos de aprendizaje profundo.

| Id | Origen | Descripción | Probabilidad | Severidad | Prioridad |
|---|---|---|---|---|---|
| R01 | Gestión | Planificación incorrecta de la duración, con riesgo de finalizar después de la fecha prevista. | Media | Media | Media |
| R02 | Tecnológico | Incompatibilidades entre versiones de librerías de deep learning (TensorFlow, Keras, Transformers, CUDA Toolkit). | Alta | Alta | Alta |
| R03 | Tecnológico | Dificultad en la integración de los módulos de entrenamiento Python con el backend FastAPI. | Media | Alta | Alta |
| R04 | Gestión | Subestimación del tiempo de entrenamiento de los modelos de deep learning, especialmente en los Sprints de validación cruzada. | Alta | Alta | Alta |
| R05 | Tecnológico | Dataset médico no disponible, inadecuado o con licencia incompatible para las pruebas de validación. | Media | Media | Media |
| R06 | Tecnológico | Bloqueo o degradación de la interfaz web durante la ejecución prolongada de un entrenamiento. | Baja | Media | Baja |
| R07 | Externo | Pérdida de código fuente por fallo del sistema de archivos o del equipo de desarrollo. | Baja | Muy Alta | Alta |
| R08 | Infraestructura | Sobrecalentamiento o agotamiento de recursos de la GPU durante entrenamientos prolongados, provocando interrupciones. | Media | Alta | Alta |
| R09 | Tecnológico | Falta de convergencia o rendimiento insuficiente de los modelos entrenados, que limita los resultados del benchmarking. | Media | Alta | Alta |

*Tabla 2 - Identificación y evaluación de riesgos del proyecto*

## 6.3 Plan de mitigación (medidas preventivas)

El plan de mitigación reúne las medidas preventivas previstas para reducir la probabilidad de cada riesgo o limitar sus efectos.

Frente al riesgo de una planificación incorrecta (R01), el alumno revisa el avance al cierre de cada Sprint junto con el tutor y compara el trabajo realizado con el previsto. Si se observa una desviación relevante, el alumno ajusta manualmente el cronograma y la carga pendiente antes de continuar con la siguiente iteración.

Para reducir las incompatibilidades entre librerías de aprendizaje profundo (R02), se fijan las versiones de las dependencias y se utilizan entornos virtuales de Anaconda. Además, durante el Sprint 1 se comprueba la compatibilidad de las librerías antes de construir el motor de inferencia.

Ante la dificultad de integrar los módulos de Python con el backend FastAPI (R03), los scripts de entrenamiento se ejecutan como procesos independientes de la capa web. Durante el Sprint 4 se comprueba la comunicación entre la API y los scripts antes de ampliar el resto de los endpoints.

Para reducir el efecto de la subestimación del tiempo de entrenamiento (R04), el trabajo comienza con arquitecturas más ligeras, como MobileNetV2 y EfficientNetB0. Sus tiempos de ejecución permiten calibrar el hardware y revisar el alcance del benchmarking antes de abordar modelos de mayor coste.

Respecto a la posible indisponibilidad del conjunto de datos médicos (R05), las radiografías se descargan localmente durante el Sprint 1. También se comprueban su formato, integridad y condiciones de uso, para reducir la dependencia de los repositorios externos durante el desarrollo.

Para evitar el bloqueo de la interfaz durante los procesos de cálculo prolongados (R06), las tareas pesadas se ejecutan de forma asíncrona. FastAPI delega estas operaciones al sistema de trabajos y la interfaz consulta su estado y progreso.

Frente a la pérdida de código fuente (R07), el proyecto utiliza un repositorio privado en GitHub y realiza copias de seguridad periódicas en un dispositivo externo. Los cambios relevantes se registran mediante commits descriptivos.

Para reducir el sobrecalentamiento o el agotamiento de recursos de la GPU (R08), las ejecuciones se separan mediante pausas y se controla la temperatura del equipo. Las arquitecturas más exigentes se ejecutan en periodos concretos y bajo supervisión.

Finalmente, para reducir el riesgo de falta de convergencia (R09), durante los sprints de entrenamiento se monitorizan las curvas de pérdida. El código utiliza parada temprana y reducción de la tasa de aprendizaje cuando detecta estancamiento. Las configuraciones iniciales de hiperparámetros se documentan y se ajustan a partir de los resultados de las primeras ejecuciones.

## 6.4 Plan de contingencia (medidas correctoras)

El plan de contingencia recoge las medidas correctoras que se aplican cuando un riesgo se materializa, con el fin de limitar sus efectos y mantener un alcance asumible para el proyecto.

**R01 – Desviación temporal**: Si el cronograma se desvía, el alumno revisa manualmente la ruta crítica y reduce, si es necesario, los elementos no esenciales, como variantes adicionales de Transformer o mejoras gráficas. La reducción del alcance se documenta y justifica en la memoria.

**R02 – Conflicto de librerías**: Si aparece una incompatibilidad entre versiones, se aísla la dependencia afectada y se consulta la documentación oficial para identificar una combinación compatible. Si es necesario, se crea un entorno de Anaconda con las versiones fijadas y se repiten las pruebas de compatibilidad antes de continuar. La configuración utilizada y la solución adoptada se registran para poder reproducir el entorno del proyecto.

**R03 – Fallo en la integración del backend**: Si la integración presenta problemas, los scripts de entrenamiento se mantienen como procesos independientes, invocados desde FastAPI mediante el módulo de subprocesos (`subprocess`). Esta separación permite comprobar la comunicación entre la API y los scripts por partes.

**R04 – Tiempo de cómputo insuficiente**: El riesgo se materializó durante el benchmarking. El alcance se redujo al subconjunto de ocho arquitecturas CNN con resultados conservados (ResNet50, DenseNet121, EfficientNetB0, EfficientNetV2B0, MobileNetV2, InceptionV3, Xception y ConvNeXtTiny), mientras que las arquitecturas restantes, incluidos los Transformers, quedaron fuera de la ejecución documentada. Esta reducción se recoge en la memoria para presentar los resultados como una evaluación parcial.

**R05 – Cambio o indisponibilidad del dataset**: Si los datos dejan de estar disponibles o no cumplen las condiciones previstas, no se sustituyen automáticamente. Primero se identifica un conjunto alternativo que sea accesible, anonimizado, compatible con la licencia y adecuado al problema clínico. Si se adopta, se repiten el entrenamiento, la validación cruzada, la validación externa y los análisis de explicabilidad, y se documenta el cambio y su efecto sobre la interpretación de los resultados.

**R06 – Bloqueo de la interfaz gráfica**: Si una tarea pesada bloquea la interfaz, se revisa su ejecución mediante la cola asíncrona y se comprueba el estado del worker. Si el bloqueo persiste, se informa al usuario del estado de la tarea y se registra la incidencia para ajustar la configuración del proceso.

**R07 – Pérdida del código fuente**: Ante un fallo del equipo, se recupera el último estado disponible desde GitHub y se restaura el entorno de trabajo. A continuación, se revisa el trabajo pendiente y se reajusta el Sprint afectado.

**R08 – Sobrecalentamiento o falta de recursos de la GPU**: Se interrumpe el entrenamiento si la temperatura o el consumo de recursos alcanza un nivel problemático. Las ejecuciones se dividen en bloques más pequeños y, si es necesario, se reducen el tamaño de lote (`batch size`) o el número de épocas.

**R09 – Falta de convergencia de un modelo**: El desarrollador revisa las tasas de aprendizaje, el preprocesamiento y la configuración de validación. Si el modelo no converge después de los ajustes previstos, se excluye del resultado consolidado o se presenta como resultado no concluyente. La sustitución de la arquitectura y la repetición completa del protocolo quedan como trabajo posterior.
