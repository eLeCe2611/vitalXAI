# Capítulo 6: Identificación y Mitigación de Riesgos

Una actividad ineludible dentro de la planificación de cualquier proyecto radica en la gestión exhaustiva de los riesgos. Esta exigencia se multiplica críticamente cuando el sistema incorpora tecnologías de altísima complejidad técnica, como ocurre en este caso con el aprendizaje profundo, la inteligencia artificial explicable y la integración simultánea de múltiples arquitecturas algorítmicas. Se define formalmente como riesgo a cualquier evento latente que, de materializarse, impactaría negativamente sobre el alcance, la planificación temporal, la calidad técnica o el coste global del proyecto. El objetivo de este apartado no persigue la erradicación total de los riesgos, un escenario operativamente imposible en un desarrollo de esta envergadura. La meta consiste en identificar anticipadamente todas las amenazas, evaluando objetivamente su probabilidad y su impacto, para estructurar un plan de actuación sólido que reduzca las posibilidades de fallo y garantice una respuesta protocolizada y ordenada si terminan sucediendo.

Para cada una de las amenazas identificadas, la estrategia de defensa establece dos protocolos diferenciados: el plan de mitigación y el plan de contingencia. El plan de mitigación engloba las acciones estrictamente preventivas que se deben ejecutar antes de que el evento adverso ocurra, buscando asfixiar su probabilidad de aparición o reducir drásticamente su impacto. Por su parte, el plan de contingencia dicta las acciones reactivas y de contención que se despliegan una vez que el riesgo ya se ha materializado de manera inevitable, con el objetivo estricto de minimizar su efecto destructivo sobre el avance del proyecto.

## 6.1 Escala de valoración de riesgos

Antes de exponer el catálogo de amenazas identificadas, resulta imperativo establecer la métrica de evaluación. El sistema define una escala estricta para cuantificar la probabilidad, la severidad y la prioridad de cada riesgo, eliminando así cualquier margen de ambigüedad en su interpretación empírica.

La probabilidad mide la viabilidad de que la amenaza logre materializarse durante el ciclo de vida del proyecto. Se divide en tres umbrales:

- **Baja**: El escenario desencadenante resulta estadísticamente anómalo o se encuentra bajo un control técnico absoluto.
- **Media**: Existe una posibilidad empírica y real de que el evento adverso quiebre las defensas bajo condiciones operativas específicas.
- **Alta**: El vector de fallo representa una vulnerabilidad común, recurrente e inherente a los desarrollos de esta naturaleza tecnológica.

La severidad cuantifica el impacto destructivo sobre el sistema si el riesgo logra ejecutar su amenaza. Se estructuran cuatro niveles de daño:

- **Baja**: Desviación superficial. El ecosistema absorbe el impacto de manera orgánica sin exigir alteraciones significativas.
- **Media**: Alteración notable. El impacto penaliza el tiempo, el coste o la calidad del código, exigiendo maniobras tácticas de corrección para garantizar la continuidad operativa.
- **Alta**: Daño crítico. El evento adverso compromete de forma grave uno o varios pilares fundamentales del proyecto, forzando un replanteamiento estructural o temporal.
- **Muy Alta**: Colapso. La materialización del riesgo amenaza de muerte la viabilidad integral del proyecto o destruye por completo la validez matemática y clínica de los resultados.

Finalmente, la prioridad fusiona ambos vectores (probabilidad y severidad). Esta intersección determina el nivel de alerta y el rigor del blindaje que exige cada amenaza, cristalizando en la matriz de evaluación que se expone en la siguiente tabla:

| Probabilidad \ Severidad | Baja | Media | Alta | Muy Alta |
|---|---|---|---|---|
| Baja | Baja | Baja | Media | Alta |
| Media | Baja | Media | Alta | Alta |
| Alta | Media | Alta | Alta | Muy Alta |

*Tabla 1 - Matriz de Prioridad*

## 6.2 Catálogo de riesgos identificados

A continuación, se presentan los riesgos identificados para este proyecto, clasificados por su origen, evaluados según su probabilidad de materialización y la severidad de su impacto, y priorizados aplicando la matriz del apartado anterior. Se han detectado un total de nueve riesgos, que abarcan desde la gestión y planificación del proyecto hasta aspectos puramente tecnológicos, incluyendo la incompatibilidad de librerías, la disponibilidad de los conjuntos de datos médicos y el rendimiento de los modelos de aprendizaje profundo.

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

## 6.3 Plan de mitigación (medidas preventivas)

El plan de mitigación orquesta la barrera defensiva del proyecto. Reúne las medidas preventivas exigidas antes de que la amenaza logre materializarse, con el objetivo innegociable de asfixiar su probabilidad de ocurrencia o amortiguar drásticamente su impacto estructural.

Frente al riesgo de una planificación incorrecta (R01), el sistema impone hitos de control estrictos. El cierre de cada Sprint exige una revisión con el tutor para auditar el progreso real frente al teórico. Si el algoritmo de gestión detecta una desviación acumulada superior al quince por ciento, el cronograma sufre una reestructuración táctica inmediata antes de autorizar el avance hacia la siguiente iteración, garantizando un ajuste realista de la carga pendiente.

Para neutralizar las incompatibilidades entre librerías de aprendizaje profundo (R02), el código ancla las versiones exactas de todas las dependencias desde el minuto cero. El despliegue exige entornos virtuales de Anaconda herméticamente aislados para evitar la contaminación del sistema anfitrión. Adicionalmente, el Sprint 1 ejecuta pruebas de estrés de compatibilidad antes de permitir la construcción del motor de inferencia, erradicando los conflictos desde la base.

Ante la dificultad de integrar los módulos de Python con el backend FastAPI (R03), la arquitectura del Sprint 1 impone una separación quirúrgica entre la capa web y la computación científica. Los algoritmos se invocan como procesos autónomos. El Sprint 4 arranca con una prueba de concepto implacable, validando la fluidez de las comunicaciones entre la API y los scripts de entrenamiento antes de autorizar el desarrollo del resto de los endpoints.

Para combatir la subestimación del tiempo de entrenamiento (R04), el calendario impone una escalada táctica. El motor computa primero las arquitecturas más ligeras (MobileNetV2, EfficientNetB0) para calibrar el hardware, antes de liberar a los colosos pesados (ConvNeXt-Tiny, Transformer). El final del Sprint 4 marca un punto de control ineludible para recalcular las proyecciones temporales futuras basándose exclusivamente en el rendimiento empírico del silicio.

Respecto a la potencial indisponibilidad del conjunto de datos médicos (R05), el protocolo exige la extracción y descarga local de las radiografías durante el Sprint 1. El sistema audita el formato, la integridad estructural y los permisos de licencia. Mantener el volumen de datos anclado en el disco duro local blinda al proyecto frente a caídas de red o alteraciones imprevistas en los repositorios externos durante todo el ciclo de desarrollo.

Para impedir el bloqueo de la interfaz durante los masivos ciclos de cálculo (R06), el diseño estructural asume un paradigma estrictamente asíncrono. FastAPI delega el procesamiento pesado a tareas en segundo plano. El sistema inyecta mecanismos de sondeo continuo y despliega telemetría de progreso en tiempo real sobre el panel de control, desterrando cualquier riesgo de congelación gráfica desde la fase de diseño.

Frente a la amenaza catastrófica de pérdida de código fuente (R07), el protocolo despliega un repositorio privado en GitHub desde el primer día. La normativa impone la ejecución de un commit descriptivo al clausurar cada jornada de trabajo, sin excepciones. Esta red de seguridad se refuerza mediante el volcado sistemático de una copia de seguridad semanal en un hardware de almacenamiento externo.

Para evitar el colapso térmico o el estrangulamiento de la GPU (R08), el motor de ejecución inyecta periodos de latencia programados entre las distintas arquitecturas para disipar el calor del hardware. Herramientas de telemetría auditan la temperatura del procesador gráfico en tiempo real. Las arquitecturas más exigentes quedan relegadas a ventanas temporales de ejecución bajo supervisión humana estricta y activa.

Finalmente, para mitigar el fracaso en la convergencia matemática de los modelos (R09), los sprints de entrenamiento despliegan un sistema de alerta temprana: el Sprint 4 para las arquitecturas CNN y el Sprint 5 para los Transformers. El código monitoriza las curvas de pérdida desde las primeras épocas y utiliza parada temprana y reducción de la tasa de aprendizaje cuando detecta estancamiento. Como línea de base, los algoritmos arrancan con configuraciones de hiperparámetros documentadas y revisadas durante las primeras ejecuciones, que se ajustan cuando los resultados experimentales evidencian problemas de convergencia.

## 6.4 Plan de contingencia (medidas correctivas)

El plan de contingencia actúa como la última línea de defensa. Despliega maniobras reactivas y de contención una vez que la amenaza ha logrado fracturar las medidas preventivas, con el objetivo innegociable de minimizar el daño estructural y garantizar la supervivencia del proyecto.

**R01 – Desviación temporal consolidada**: Si el cronograma colapsa, el sistema aplica una poda táctica. Se ejecuta una revisión inmediata de la ruta crítica, amputando el alcance de los elementos no esenciales (variantes accesorias de Transformer o florituras gráficas de la interfaz). El objetivo es salvaguardar la entrega de un núcleo plenamente funcional. Esta reducción del alcance se documentará y justificará explícitamente en la memoria.

**R02 – Conflicto estructural de librerías**: En el caso de que se produzca un conflicto de incompatibilidad entre versiones de librerías (R02), el protocolo de actuación se estructura en tres niveles. En primer lugar, se aísla la dependencia conflictiva y se consulta la documentación oficial de las librerías implicadas para identificar la combinación de versiones compatible, estableciendo un plazo máximo de cuarenta y ocho horas para localizar la solución. En segundo lugar, la resolución del conflicto se apoya en el uso de entornos virtuales de Anaconda: se crea un entorno conda aislado en el que se instalan las versiones exactas de las dependencias, de modo que la combinación compatible se despliega y valida en ese entorno sin contaminar el resto de instalaciones de la máquina anfitriona, garantizando además la reproducibilidad de los experimentos. En tercer lugar, el despliegue del sistema se apoya en la estrategia de exposición del servicio: vitalXAI se publica a través de un túnel de Cloudflare que expone el servicio alojado en el servidor local, de modo que el entorno de ejecución (versiones de librerías, configuración del toolkit de CUDA y entorno Python) queda confinado y validado en la máquina de despliegue antes de que el servicio se publique a través del túnel. Este diseño garantiza que la versión del sistema que llega a los usuarios se ejecute siempre sobre un entorno controlado y coherente, permitiendo corregir y verificar cualquier incompatibilidad de versiones en la máquina anfitriona con total trazabilidad antes de exponer el servicio.

**R03 – Fractura en la integración del backend**: Si el acoplamiento orgánico fracasa, el diseño adopta una arquitectura de trinchera. Los scripts de entrenamiento se encapsulan herméticamente como procesos independientes, invocados desde FastAPI mediante el módulo de subprocesos (subprocess). Esta cirugía informática desacopla por completo la carga computacional de la petición web, permitiendo validar la comunicación capa por capa.

**R04 – Estrangulamiento del tiempo computacional**: Si el silicio no cumple las proyecciones de velocidad, el alcance del benchmarking sufre un recorte quirúrgico. La evaluación masiva se limitará a un subconjunto representativo (por ejemplo, dos arquitecturas CNN y un Transformer), salvaguardando la demostración de viabilidad del concepto. Las arquitecturas restantes quedarán relegadas a trabajo futuro, dejando constancia de esta limitación técnica en la memoria.

**R05 – Incompatibilidad sobrevenida del dataset**: Ante la corrupción o inutilidad de los datos anclados en las pruebas de validación, la contingencia no puede consistir en un cambio automático de conjunto de datos. Sustituir una cohorte médica por otra altera el protocolo clínico y de validación del estudio: un conjunto de datos distinto introduce variaciones en la población, el equipo de adquisición y los criterios de etiquetado, por lo que cualquier resultado obtenido sin volver a ejecutar el protocolo completo carecería de validez científica. Por ello, la actuación consiste en identificar un conjunto de datos alternativo que cumpla los requisitos del estudio —disponibilidad, anonimización, licencia compatible y coherencia con el problema clínico— y, en caso de adoptarse, reejecutar de forma íntegra el pipeline de entrenamiento, la validación cruzada, la validación externa y los análisis de explicabilidad sobre la nueva cohorte, con la trazabilidad y la reproducibilidad exigidas en la metodología. Cualquier cambio de dataset y sus implicaciones sobre la interpretación de los resultados se documentarán de forma explícita y rigurosa en la memoria, de modo que el estudio no presente resultados que no provengan de un protocolo íntegramente validado.

**R06 – Congelación de la interfaz gráfica**: Si la sobrecarga algorítmica logra bloquear el frontend durante las pruebas de integración, la implementación de colas asíncronas asume máxima e inmediata prioridad. Si el reloj del Sprint impide una solución estructural definitiva, el código inyectará un parche preventivo: un panel de advertencia informando al clínico sobre el tiempo estimado de espera y habilitando la consulta del estado en diferido.

**R07 – Destrucción física del código fuente**: Ante un fallo catastrófico del hardware del equipo, el protocolo de recuperación extrae de urgencia el último estado seguro desde el repositorio privado en GitHub hacia una máquina de soporte. Tras restablecer el entorno de trabajo, se cuantifica el volumen del código evaporado y se reestructura internamente el Sprint en curso para absorber el impacto sin alterar la fecha de entrega.

**R08 – Colapso térmico de la GPU**: El sistema ordena una interrupción instantánea del entrenamiento para purgar el calor del procesador gráfico y salvar su integridad. Los ciclos computacionales masivos se fragmentarán en bloques más pequeños con pausas de refrigeración obligatorias. Si la asfixia del hardware persiste, el algoritmo ejecutará un recorte drástico sobre el tamaño de los lotes (batch size) o el límite de épocas.

**R09 – Fracaso en la convergencia matemática**: El algoritmo entra en cuarentena investigativa. El desarrollador audita de forma sistemática las tasas de aprendizaje, las capas de preprocesamiento y la hermeticidad de las fronteras de validación. Dado que el benchmarking final no dispone de una reserva temporal para reentrenar de nuevo las diecinueve arquitecturas, si un modelo se niega a aprender tras los ajustes permitidos se excluirá del resultado consolidado o se presentará como resultado no concluyente, dejando constancia explícita de la incidencia. La sustitución de la arquitectura y la reejecución completa del protocolo quedan como trabajo posterior, no como una contingencia ejecutable dentro del calendario de entrega.
