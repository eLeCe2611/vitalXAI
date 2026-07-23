# Capítulo 6: Identificación y Mitigación de Riesgos

Una actividad esencial dentro de la planificación de cualquier proyecto es la gestión de los riesgos, sobre todo cuando incorpora tecnologías con un alto componente técnico como puede ser, en el caso de este proyecto, el deep learning, la inteligencia artificial explicable y la integración de múltiples arquitecturas de modelos. Se considera un riesgo a cualquier evento que, si sucede, puede afectar de manera negativa al alcance, planificación, calidad o coste del proyecto. El objetivo de este apartado no es eliminar los riesgos, ya que en un proyecto de estas características es imposible, sino identificar todos aquellos que puedan suceder de manera anticipada, valorando tanto su probabilidad como impacto, y disponer de un plan de actuación claro para reducir la posibilidad de que ocurran y para responder de manera ordenada en caso de que se materialicen.

Para cada uno de los riesgos identificados se distinguen dos planes: el plan de mitigación y el plan de contingencia. El plan de mitigación recoge las acciones preventivas que se deben ejecutar antes de que ocurra el riesgo para reducir su probabilidad o impacto. El plan de contingencia ejecuta las acciones una vez que el riesgo ya se ha materializado, con el objetivo de minimizar su efecto sobre el proyecto.

## 6.1 Cuadro de valoración de riesgos

Antes de presentar los riesgos identificados, se define la escala utilizada para valorar la probabilidad, severidad y prioridad de cada uno de ellos, con el fin de que no haya ambigüedades en su interpretación.

La probabilidad es la responsable de calcular la posibilidad de que el riesgo se materialice durante el desarrollo del proyecto. El riesgo tiene una probabilidad baja si el escenario que lo provoca es poco frecuente o se encuentra controlado. Cuando hay una probabilidad real de que un riesgo ocurra bajo ciertas condiciones dentro del proyecto, se dice que tiene una probabilidad media. Cuando el escenario que produce un riesgo es común en proyectos de este tipo, la probabilidad de que ocurra será elevada.

La severidad estima el impacto que tendrán los riesgos sobre el proyecto si estos llegan a materializarse. Se distinguen cuatro niveles. La severidad baja implica una desviación menor que puede absorberse sin ajustes significativos. La severidad media causará una desviación notable en tiempo, coste o calidad, pero el proyecto podrá continuar tras realizar algunos ajustes. Si la severidad es alta, compromete de manera seria uno o varios objetivos del proyecto, requiriendo un replanteamiento parcial. Por último, la severidad muy alta pone en riesgo la viabilidad del proyecto o la integridad de los resultados.

La prioridad combina la probabilidad y la severidad para determinar el nivel de atención que requiere cada riesgo, tal y como se recoge en la siguiente tabla:

| Probabilidad \ Severidad | Baja | Media | Alta | Muy Alta |
|---|---|---|---|---|
| Baja | Baja | Baja | Media | Alta |
| Media | Baja | Media | Alta | Alta |
| Alta | Media | Alta | Alta | Muy Alta |

*Tabla 1 - Matriz de Prioridad*

## 6.2 Riesgos Identificados

A continuación, se presentan los riesgos identificados para este proyecto, clasificados según su origen, valorados en función de la probabilidad de que se materialicen y de la severidad de su impacto en caso de suceder, y priorizados aplicando la matriz de evaluación definida en el apartado anterior. Se han identificado un total de nueve riesgos, que abarcan desde aspectos relacionados con la gestión y planificación del proyecto hasta aspectos puramente tecnológicos, incluyendo riesgos de compatibilidad de librerías, disponibilidad de datasets médicos y rendimiento de los modelos de deep learning.

| Id | Origen | Descripción | Probabilidad | Severidad | Prioridad |
|---|---|---|---|---|---|
| R01 | Gestión | Planificación incorrecta de la duración, terminando el proyecto después de la fecha prevista. | Media | Media | Media |
| R02 | Tecnológico | Incompatibilidades entre versiones de librerías de deep learning (TensorFlow, Keras, Transformers, CUDA Toolkit). | Alta | Alta | Alta |
| R03 | Tecnológico | Dificultad en la integración de los módulos de entrenamiento Python con el backend FastAPI. | Media | Alta | Alta |
| R04 | Gestión | Subestimación del tiempo de entrenamiento de los modelos de deep learning, especialmente en los Sprints de validación cruzada. | Alta | Alta | Alta |
| R05 | Tecnológico | Dataset médico no disponible, inadecuado o con licencia incompatible para las pruebas de validación. | Media | Media | Media |
| R06 | Tecnológico | Bloqueo o degradación de la interfaz web durante la ejecución prolongada de un entrenamiento. | Baja | Media | Baja |
| R07 | Externo | Pérdida de código fuente por fallo del sistema de archivos o del equipo de desarrollo. | Baja | Muy Alta | Alta |
| R08 | Infraestructura | Sobrecalentamiento o agotamiento de recursos de la GPU durante entrenamientos prolongados, provocando interrupciones. | Media | Alta | Alta |
| R09 | Tecnológico | Falta de convergencia o rendimiento insuficiente de los modelos entrenados, invalidando los resultados del benchmarking. | Media | Alta | Alta |

*Tabla 2 - Identificación y evaluación de riesgos del proyecto*

## 6.3 Plan de mitigación

El plan de mitigación tiene la responsabilidad de reunir las medidas preventivas que deben llevarse a cabo antes de que cada riesgo se materialice, con el objetivo de disminuir su ocurrencia o limitar su posible impacto en el proyecto.

En lo relativo a la posible planificación incorrecta (R01), para reducir la probabilidad de que se produzca una desviación temporal significativa se van a establecer hitos de revisión al cierre de cada uno de los Sprints en las reuniones con el tutor, evaluando el progreso real frente al planificado. En caso de detectarse una desviación acumulada superior al quince por ciento de las horas planificadas originalmente, se realizará una revisión del cronograma antes de continuar con el siguiente Sprint, ajustando las tareas pendientes de manera más realista.

En cuanto a las posibles incompatibilidades entre versiones de librerías de deep learning (R02), con el objetivo de evitar conflictos de compatibilidad durante el desarrollo se fijarán desde el inicio del proyecto las versiones exactas de todas las dependencias en el archivo de requisitos. Además, se utilizarán entornos virtuales aislados para no interferir con otras instalaciones del equipo y se ejecutarán pruebas de compatibilidad durante el Sprint 1, antes de abordar la implementación del motor de inferencia.

Respecto a la posible dificultad para integrar los módulos de entrenamiento Python con el backend FastAPI (R03), para minimizar este riesgo se diseñará la arquitectura del sistema desde el Sprint 1 contemplando explícitamente la separación entre la capa web y los módulos de computación científica, de forma que estos se puedan invocar como procesos independientes. Al inicio del Sprint 4 se realizará una prueba de concepto de integración antes de desarrollar el resto de endpoints, validando que la comunicación entre la API y los scripts de entrenamiento funciona correctamente.

En relación con la posible subestimación del tiempo de entrenamiento de los modelos (R04), se va a priorizar el orden de implementación comenzando por las arquitecturas más ligeras (MobileNetV2, EfficientNetB0) antes de abordar las más pesadas (ConvNeXt-Tiny, Transformer), acumulando experiencia sobre los tiempos reales de entrenamiento. Se establecerá un hito intermedio de revisión al finalizar el Sprint 4 para reevaluar si las estimaciones de tiempo para los Sprints siguientes siguen siendo realistas.

En lo que respecta a la posible indisponibilidad o inadecuación del dataset médico (R05), la mitigación consistirá en preseleccionar y descargar de manera local los datasets necesarios durante la fase de análisis del Sprint 1, verificando su formato, estructura y licencia de uso. El hecho de disponer de los datasets descargados localmente desde el inicio del proyecto garantiza su disponibilidad sin depender de la conectividad ni de cambios en los repositorios online durante el desarrollo.

Sobre el posible bloqueo de la interfaz durante ejecuciones largas de entrenamiento (R06), la arquitectura frontend-backend que se diseñará durante el Sprint 1 contemplará la ejecución asíncrona de los entrenamientos mediante BackgroundTasks de FastAPI, un sistema de consulta de estado y la visualización de indicadores de progreso en la interfaz, de forma que el bloqueo quede descartado desde una fase temprana del desarrollo.

Frente al riesgo de pérdida de código fuente (R07), se configurará un repositorio privado en GitHub desde el primer día del proyecto y se establecerá como práctica obligatoria realizar un commit al final de cada sesión de trabajo, con un mensaje descriptivo del avance realizado. Adicionalmente, se configurará una copia de seguridad semanal del repositorio en un almacenamiento externo.

Para prevenir el sobrecalentamiento o agotamiento de recursos de la GPU durante entrenamientos prolongados (R08), se implementarán pausas programadas entre entrenamientos de distintas arquitecturas para permitir la refrigeración del equipo, y se monitorizará la temperatura de la GPU durante las ejecuciones mediante herramientas de vigilancia del sistema. Los entrenamientos más intensivos se programarán en sesiones con supervisión activa.

Con el fin de mitigar el riesgo de falta de convergencia o rendimiento insuficiente de los modelos (R09), se establecerá desde el Sprint 2 un conjunto de métricas de validación temprana que permitan detectar problemas de entrenamiento en las primeras épocas, incluyendo la monitorización de la pérdida en entrenamiento y validación para identificar sobreajuste o falta de aprendizaje. Además, se definirán hiperparámetros por defecto contrastados en la literatura científica como punto de partida para todos los modelos.

## 6.4 Plan de contingencia

El plan de contingencia se ocupa de tomar las medidas correctivas que deben implementarse una vez que el riesgo se ha concretado, con el fin de reducir al mínimo su efecto sobre el proyecto y asegurar la continuidad del desarrollo.

En el caso de que la desviación temporal (R01) sea ya un hecho consolidado, se realizará una revisión del cronograma completo para identificar las tareas del camino crítico, reduciendo o descartando el alcance de aquellas que no sean esenciales para la entrega, como por ejemplo la implementación de algunas variantes Transformer o funcionalidades accesorias de la interfaz gráfica, priorizando siempre la entrega de un sistema funcional que demuestre el concepto completo. Esta decisión se documentará de manera explícita en la memoria del TFG, describiendo el alcance real entregado frente al planificado.

En el caso de que se produzca un conflicto de incompatibilidad entre versiones de librerías (R02), se aislará la dependencia problemática y se consultará la documentación oficial de cada librería para identificar la combinación de versiones compatible. En caso de que no se encuentre solución en un plazo máximo de dos días, se evaluará la sustitución de la librería afectada por una alternativa técnicamente equivalente. Por ejemplo, si una versión de TensorFlow resulta incompatible con la GPU disponible, se considerará el uso de TensorFlow con soporte CPU o la migración a PyTorch para los modelos Transformer.

Si la integración de los scripts de entrenamiento en el backend (R03) resultara finalmente inviable por la vía directa, se encapsularán dichos scripts como procesos independientes invocados desde el backend mediante subprocess, desacoplando completamente la ejecución del entrenamiento de la petición web. La integración se llevará a cabo de manera incremental, validando capa por capa hasta garantizar el correcto funcionamiento del sistema completo.

En el supuesto de que la subestimación del tiempo de entrenamiento (R04) se materialice, se reducirá el alcance del benchmarking a un subconjunto representativo de arquitecturas (por ejemplo, dos CNN y un Transformer) que permita demostrar la validez del concepto y obtener conclusiones significativas, posponiendo la evaluación completa de todas las arquitecturas para trabajo futuro. Esta decisión será documentada explícitamente en la memoria.

Si en el momento de realizar las pruebas de validación los datasets descargados presentaran problemas de formato o incompatibilidad (R05), se recurrirá a datasets alternativos del mismo repositorio, aplicando las transformaciones necesarias. En caso de ser requerido, se documentará en la memoria la naturaleza del dataset utilizado, sus características y las limitaciones que su uso introduce en la interpretación de los resultados.

En el caso de que el bloqueo de la interfaz durante ejecuciones largas (R06) se produzca en las pruebas de integración, se implementará de forma prioritaria el mecanismo de ejecución asíncrona y los indicadores de progreso. Si las restricciones de tiempo del Sprint no permitieran una solución completa, se añadirá como medida temporal un mensaje informativo al usuario indicando el tiempo estimado de espera y la posibilidad de consultar el estado posteriormente.

Si se produjese una pérdida de código fuente como consecuencia de un fallo del equipo de desarrollo (R07), se procederá a clonar el repositorio de GitHub en un equipo de sustitución, recuperando así el último estado confirmado del proyecto. Una vez recuperado el entorno de trabajo, se evaluará el volumen de trabajo perdido y se replanificarán las tareas afectadas dentro del Sprint en curso.

En caso de que se produzca una interrupción por sobrecalentamiento o agotamiento de recursos de la GPU (R08), se detendrá el entrenamiento de manera inmediata para permitir la refrigeración del equipo y se evaluará el estado del modelo antes de la interrupción. Los entrenamientos más largos se fragmentarán en sesiones más cortas con pausas intermedias, y se considerará la reducción del número de épocas o del tamaño de lote si el problema persiste.

Si los modelos entrenados no alcanzaran un rendimiento suficiente o no convergieran adecuadamente (R09), se realizará un análisis sistemático de las causas: revisión de la arquitectura del modelo, ajuste de la tasa de aprendizaje, verificación del preprocesamiento de los datos y comprobación de la correcta separación entre conjuntos de entrenamiento y validación. En caso de que el problema persista tras varios intentos de ajuste, se considerará la sustitución de la arquitectura problemática por una alternativa contrastada en la literatura. Este resultado se documentará y analizará en la memoria como un hallazgo técnico relevante sobre la aplicabilidad de la arquitectura al dominio de la imagen médica.
