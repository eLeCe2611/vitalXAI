# Capítulo 4: Marco Metodológico de Gestión

## 4.1 Fundamentación del Enfoque Metodológico

La naturaleza de este proyecto combina desarrollo de software con investigación computacional aplicada al diagnóstico por imagen médica, lo que implica un grado de incertidumbre técnica inherente, ya que el comportamiento de las distintas arquitecturas de deep learning frente a los conjuntos de datos de entrenamiento no siempre es predecible, y los resultados del benchmarking pueden requerir que se realicen ajustes en el diseño que no se pueden anticipar desde un inicio. A esto se le suma que el proyecto cuenta únicamente con un desarrollador y tiene una duración acotada, lo que implica que metodologías de gran peso procedimental, por ejemplo, Métrica V3, resulten desproporcionadas para la escala de trabajo.

Por tanto, se ha adoptado una metodología ágil, concretamente el framework Scrum (Schwaber & Sutherland, 2020), que se complementará con un tablero Kanban como herramienta de gestión visual del flujo de trabajo. Tres motivos específicos justifican la elección de Scrum sobre un enfoque más tradicional en cascada. El primero es el componente exploratorio del desarrollo, particularmente en lo relacionado con la comparación de arquitecturas CNN y Transformer y con el ajuste de hiperparámetros, lo que implica la necesidad de tener adaptabilidad para reorientar los esfuerzos basándose en los resultados obtenidos en cada uno de los ciclos. La segunda razón guarda relación con la estructura iterativa que proporciona Scrum, pues esta posibilita la detección y rectificación de fallos en las fases tempranas, lo que provoca una disminución de la probabilidad de que el producto final no cumpla con los objetivos establecidos. En tercer lugar, la literatura ha evidenciado que Scrum puede implementarse de manera satisfactoria en contextos de desarrollo individual, realizando una modificación de las ceremonias y los roles, pero sin sacrificar las ventajas intrínsecas del marco de trabajo.

## 4.2 Implementación del Marco Scrum en el Proyecto

Scrum es un framework ágil para el desarrollo de productos complejos definido por Ken Schwaber y Jeff Sutherland en la Scrum Guide (Schwaber & Sutherland, 2020), cuya versión vigente data del año 2020. Su estructura se organiza en torno a tres elementos: roles, eventos y artefactos.

### 4.2.1 Roles

- **Product Owner (Aurelio López Fernández)**: El tutor académico actúa como Product Owner, ya que no hay un cliente externo. Es el encargado de validar las entregas, determinar qué es lo más importante entre los componentes del sistema y establecer los criterios de aceptación para cada segmento de trabajo.
- **Scrum Master y Developer (Luis Carmona Berdugo)**: al ser un proyecto de desarrollo unipersonal, el alumno concentra ambos roles. Como Scrum Master, es el responsable de la organización del trabajo en sprints, el mantenimiento de los artefactos del proceso y la garantía de que el proyecto avanza de manera coherente con la planificación. Como Developer, asume la totalidad de la responsabilidad técnica de implementación.
- **Asesores científicos (Domingo S. Rodríguez Baena, Iván Segura-Carmona, Marc Ríos-Cadenas)**: pese a que su rol no está definido dentro de la terminología de Scrum, este podría asimilarse al de *domain experts*, que son expertos de dominio que aportan conocimiento especializado de manera puntual cuando el desarrollo lo requiera, sin necesidad de formar parte del equipo en un sentido estricto.

La dedicación de los recursos humanos en el proyecto no es uniforme a lo largo del mismo, sino que varía en función de la naturaleza de cada tarea. El alumno trabaja al 100% de la jornada en la totalidad del desarrollo, reduciéndose al 60% en la tarea inicial de planificación del proyecto y al 40% en la reunión final de cierre. El tutor, al ser el Product Owner, dedica el 60% y 40% a la reunión inicial y final respectivamente. Los asesores mantienen una dedicación constante del 25% en todas las tareas en las que intervienen, reflejando su rol de consultoría puntual y no de desarrollo continuo del sistema.

En cuanto a los recursos materiales, el proyecto requiere un equipo con capacidad de cómputo GPU para el entrenamiento de los modelos de deep learning, particularmente durante las fases de validación cruzada de las arquitecturas CNN y Transformer. Se ha empleado una estación de trabajo local equipada con una GPU NVIDIA compatible con CUDA, cuyo coste de uso está incluido en la infraestructura hardware disponible para el desarrollo del TFG, sin necesidad de recurrir a instancias de computación en la nube.

### 4.2.2 Eventos

El evento central es el Sprint, que es un ciclo iterativo de duración fija de dos semanas, tal y como se detalla en el capítulo de planificación. Cada uno de los Sprints se articula en torno a tres ceremonias: Sprint Planning, Sprint Review y Sprint Retrospective.

El Sprint Planning se realiza al inicio de cada Sprint, donde el alumno en coordinación con el tutor selecciona los elementos del Product Backlog a abordar durante ese período y los desglosa en tareas concretas que conforman el Sprint Backlog.

En el Sprint Review se presentan los incrementos completados al tutor, quien actúa como Product Owner y valida o rechaza los resultados obtenidos. Esto se realiza al final de cada Sprint.

La última de las ceremonias es la Sprint Retrospective, en la que el alumno reflexiona acerca del proceso que se ha seguido e identifica mejoras para el ciclo siguiente.

En este proyecto no se realiza ninguna Daily Scrum, ya que no resulta operativo por el hecho de ser un proyecto individual. Para sustituir estas reuniones diarias, se realizan reuniones periódicas de seguimiento con el tutor y, cuando sea necesario, con los asesores. Estas reuniones cumplen una función análoga: el alumno presenta los avances realizados, expone las dudas técnicas surgidas, recibe retroalimentación sobre los resultados obtenidos y acuerda las tareas a acometer hasta el siguiente encuentro. El registro de estas reuniones queda recogido en el anexo de seguimiento del proyecto, que actúa como bitácora formal del proceso a lo largo del ciclo de vida del desarrollo.

El programa de trabajo de este proyecto incluye una jornada laboral de seis horas al día de lunes a viernes. Los días festivos locales y nacionales del año académico 2025-2026 se consideran no laborables, lo que incluye el receso navideño entre el 22 de diciembre de 2025 y el 6 de enero de 2026.

### 4.2.3 Artefactos

- **Product Backlog**: es una lista ordenada y priorizada de todo el trabajo pendiente, compuesta por los requisitos funcionales y no funcionales del sistema, las tareas de implementación de los pipelines de entrenamiento para arquitecturas CNN y Transformer, los módulos de generación de explicaciones XAI, los experimentos de benchmarking planificados y los documentos del TFG pendientes de elaboración. Es gestionada por el alumno y revisada de manera conjunta con el tutor en cada Sprint Planning.
- **Sprint Backlog**: es el subconjunto de elementos del Product Backlog seleccionados para el Sprint en curso, de manera que estos elementos estén desglosados en tareas concretas y estimables que guían el trabajo durante el ciclo.
- **Increment**: es el conjunto de todos los elementos que se han completado durante el Sprint, que deben cumplir con la *Definition of Done* —el criterio acordado que define cuándo una tarea puede considerarse terminada— antes de ser presentados en el Sprint Review.

## 4.3 Gestión visual del flujo de trabajo: Scrumban con GitHub Projects

Se utiliza un tablero Kanban, gestionado a través de GitHub Projects, como instrumento visual para administrar el flujo de trabajo, además del marco Scrum. La razón por la que se escoge GitHub Projects, en lugar de otras herramientas, es que el repositorio del proyecto está alojado en GitHub. Esto posibilita asociar de manera directa las tareas del tablero a los *commits*, *pull requests* e *issues* del código, unificando toda la trazabilidad del desarrollo en una sola plataforma.

El tablero está organizado en cuatro columnas que representan los estados por los que puede transitar cada una de las tareas:

- **Por Hacer (To Do)**: son las tareas planificadas para el Sprint en curso, aún no iniciadas.
- **En Progreso (In Progress)**: tareas activamente en desarrollo.
- **En Revisión (In Review)**: tareas completadas por el alumno y pendientes de validación por el tutor en la próxima reunión de seguimiento.
- **Hecho (Done)**: tareas validadas que cumplen la *Definition of Done*.

La combinación de Scrum y Kanban, denominada Scrumban en la literatura, permite aprovechar la estructura iterativa y los ritmos de inspección de Scrum junto con la visibilidad continua del flujo de trabajo que proporciona el tablero, resultando adecuada para proyectos de un único desarrollador donde la capacidad de autogestión es fundamental.

## 4.4 Alcance de la metodología

La metodología Scrum solo incluye la etapa de desarrollo activa del sistema, que se extiende desde la fase de planificación hasta la entrega y exposición final del TFG. Dado que se trata de un proyecto de investigación académica con un inicio y un final definidos, no se toma en cuenta la fase de mantenimiento posterior. El capítulo correspondiente de la memoria aborda el trabajo que se realizará en el futuro, que comprenderá las mejoras potenciales, el mantenimiento y la expansión del sistema después de la entrega del TFG.
