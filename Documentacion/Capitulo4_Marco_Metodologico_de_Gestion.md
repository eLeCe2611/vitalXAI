# Capítulo 4: Marco Metodológico de Gestión

Todo proyecto necesita un marco de gestión que ordene su ejecución, y la elección de dicho marco debe ser coherente con la naturaleza del trabajo que se va a desarrollar. Este capítulo describe cómo se gestiona el presente proyecto: los criterios que llevaron a elegir un enfoque ágil, la forma en que se adapta el marco de trabajo Scrum a un proyecto de estas características, las herramientas de seguimiento utilizadas y el alcance de la metodología. El objetivo es que la gestión no sea un mero formalismo, sino un mecanismo que aporte orden, transparencia y capacidad de adaptación al desarrollo.

## 4.1 Justificación del enfoque metodológico

La naturaleza de este proyecto combina desarrollo de software con investigación computacional aplicada al diagnóstico por imagen médica. Esta doble naturaleza introduce un grado de incertidumbre técnica inherente que condiciona la elección de la metodología. Por un lado, el comportamiento de las arquitecturas de deep learning frente a los conjuntos de datos no siempre es predecible: los resultados del benchmarking pueden revelar que es necesario ajustar el diseño, los hiperparámetros o incluso el alcance de lo planificado, y estos ajustes no pueden anticiparse en su totalidad desde el inicio. Por otro lado, el proyecto cuenta con un único desarrollador y con una duración acotada, lo que descarta metodologías de gran peso procedimental, como Métrica V3, cuyo nivel de burocracia resultaría desproporcionado para la escala de trabajo. En la literatura de gestión de proyectos se reconoce que no existe un marco universal válido para todo: la metodología debe elegirse ponderando el tamaño del proyecto, la dinámica de sus requisitos y el entorno en el que se desarrolla (Boehm & Turner, 2004).

A la vista de estas características, se ha adoptado una metodología ágil, concretamente el framework Scrum (Schwaber & Sutherland, 2020), complementado con un tablero Kanban como herramienta de gestión visual del flujo de trabajo. Tres motivos específicos justifican esta elección frente a un enfoque tradicional en cascada. El primero es el componente exploratorio del desarrollo, particularmente en lo relacionado con la comparación de arquitecturas de deep learning y con el ajuste de sus hiperparámetros: la naturaleza iterativa de Scrum permite reorientar los esfuerzos sobre la base de los resultados obtenidos en cada ciclo, en lugar de quedar atados a una planificación rígida. El segundo motivo guarda relación con la estructura iterativa que proporciona Scrum, que posibilita detectar y corregir errores en fases tempranas, reduciendo la probabilidad de que el producto final no se ajuste a los objetivos establecidos. En tercer lugar, tanto la literatura empírica sobre métodos ágiles (Dybå & Dingsøyr, 2008) como la experiencia acumulada de su aplicación (Sutherland, 2014) evidencian que Scrum puede implementarse de manera satisfactoria en contextos de desarrollo individual, adaptando las ceremonias y los roles sin sacrificar las ventajas intrínsecas del marco de trabajo.

## 4.2 Roles y recursos del proyecto

### 4.2.1 Roles dentro del marco de trabajo

Scrum define tres roles con responsabilidades bien delimitadas. En este proyecto, al tratarse de un desarrollo unipersonal, la asignación de estos roles se adapta a la realidad del equipo:

- **Product Owner (Aurelio López Fernández)**: El tutor académico asume este rol ante la ausencia de un cliente externo. Él valida personalmente las entregas, jerarquiza la importancia de los componentes algorítmicos y define los criterios de aceptación que rigen cada segmento de trabajo.
- **Scrum Master y Developer (Luis Carmona Berdugo)**: Al ser un proyecto de desarrollo individual, el alumno concentra ambos roles. Como Scrum Master, es el responsable de la organización del trabajo en sprints, del mantenimiento de los artefactos del proceso y de garantizar que el proyecto avanza de manera coherente con la planificación. Como Developer, asume la totalidad de la responsabilidad técnica de la implementación.
- **Asesores científicos (consultor de persistencia y bases de datos, asesores de deep learning y XAI, de imagen médica y de ingeniería del software)**: La terminología de Scrum omite esta figura. Nosotros la asimilamos al concepto de *domain experts*. Estos especialistas inyectan conocimiento crítico puntualmente durante las encrucijadas del desarrollo, manteniendo una posición externa sin integrarse formalmente en la célula de programación.

### 4.2.2 Dedicación y recursos materiales

La dedicación de los recursos humanos no es uniforme a lo largo del proyecto, sino que varía en función de la naturaleza de cada tarea y de la participación concreta de cada persona. El alumno asume la mayor parte de la ejecución, pero su porcentaje de dedicación también se ajusta a cada actividad: en las reuniones inicial y final comparte la dedicación al 50 % con el tutor, mientras que en las tareas técnicas suele asumir el 100 %. El tutor, en su papel de Product Owner, participa al 50 % en las tareas 0.1 y 8.3. Los asesores intervienen con porcentajes variables, que en el cronograma oscilan entre el 3 %, el 5 %, el 8 %, el 10 %, el 15 % y el 25 %, según la tarea y el tipo de revisión o consulta requerida. Estas proporciones son las que sustentan el cálculo de horas y costes del apartado 5.3; no existe, por tanto, una dedicación uniforme de los asesores.

En cuanto a los recursos materiales, el proyecto requiere un equipo con capacidad de cómputo GPU para el entrenamiento de los modelos de deep learning, particularmente durante las fases de validación cruzada de las arquitecturas CNN y Transformer. Se emplea una estación de trabajo local equipada con una GPU NVIDIA compatible con CUDA, cuyo coste de uso está incluido en la infraestructura hardware disponible para el desarrollo del TFG, sin necesidad de recurrir a instancias de computación en la nube. Todo el software utilizado es de código abierto y gratuito, por lo que no se incurre en costes de licenciamiento.

## 4.3 Ciclo de trabajo iterativo

### 4.3.1 Los sprints y la cadencia del trabajo

El evento central del marco Scrum es el Sprint, entendido en este proyecto como un ciclo iterativo de trabajo con un objetivo y un incremento verificable. La aplicación es una adaptación de Scrum a un TFG unipersonal: los nueve sprints tienen duración desigual, porque la planificación real reserva más tiempo a la fase inicial, a los bloques técnicos de mayor complejidad y a la documentación final. Por tanto, no se afirma que exista una cadencia temporal fija ni que se aplique Scrum de forma ortodoxa; se conservan sus elementos útiles de planificación, revisión, retrospectiva, backlog e incremento, ajustados a las restricciones académicas y al volumen variable de cada bloque. Cada sprint procura producir un incremento potencialmente entregable, integrando diseño, implementación y pruebas cuando la naturaleza de la tarea lo permite. Las pruebas se realizan de forma continua e incremental, incluyendo las pruebas de seguridad en los mismos sprints en que se desarrollan los componentes afectados.

La ejecución de cada tarea de implementación se apoya, además, en el modelo de desarrollo basado en especificaciones y guiado por pruebas (SDD/TDD), diseñado con la colaboración del asesor de ingeniería del software y descrito en el capítulo de organización. Este modelo organiza el trabajo de programación en ciclos en los que primero se define la especificación de la funcionalidad, después se escriben las pruebas que deben satisfacerla y, finalmente, se implementa el código necesario para que esas pruebas pasen y se refactoriza el resultado (Beck, 2000). Esta práctica garantiza que cada funcionalidad quede cubierta por pruebas automatizadas y contribuye a la calidad y a la reproducibilidad del desarrollo.

### 4.3.2 Ceremonias y reuniones de seguimiento

Cada Sprint se organiza, cuando la fase y la disponibilidad de los participantes lo permiten, alrededor de las actividades adaptadas de planificación, revisión y retrospectiva. El alumno desglosa los elementos del Product Backlog en tareas concretas y utiliza el tablero para realizar el seguimiento. Las revisiones con el tutor se celebran en los hitos previstos y mediante reuniones puntuales, sin asumir dieciocho ceremonias formales con dedicación presupuestada. La retrospectiva se realiza como revisión del proceso al cierre de cada bloque cuando resulta aplicable.

En este proyecto no se realiza ninguna Daily Scrum, ya que no resulta operativo en un contexto de desarrollo individual. Para cubrir la función de estas reuniones diarias se realizan reuniones periódicas de seguimiento con el tutor y, cuando es necesario, con los asesores. En estas reuniones el alumno presenta los avances realizados, expone las dudas técnicas surgidas, recibe retroalimentación sobre los resultados obtenidos y acuerda las tareas a acometer hasta el siguiente encuentro. El registro de estas reuniones queda recogido en el Anexo de Seguimiento del Proyecto, que actúa como bitácora formal del proceso a lo largo del ciclo de vida del desarrollo.

La ejecución del proyecto no ha seguido un calendario artificialmente uniforme, sino la cadencia real que impone un trabajo académico con un único desarrollador. El proyecto se inició a finales de noviembre de 2025. Durante el periodo comprendido entre ese momento y finales de febrero de 2026, la actividad se limitó a un par de reuniones de seguimiento con el tutor y a una pequeña inicialización del marco tecnológico: la selección de las librerías, la preparación del entorno y el arranque del repositorio. A partir de principios de marzo de 2026 comenzó el desarrollo completo del sistema, que se prolongó hasta principios de junio de 2026, con algunas reuniones puntuales —pocas, pero decisivas— con el tutor y, cuando fue necesario, con los asesores, para revisar los avances y acordar los pasos siguientes. Desde principios de junio de 2026 hasta septiembre de 2026 se desarrolló la documentación completa del proyecto, junto con el benchmarking final, las correcciones y la entrega, de nuevo con algunas reuniones de seguimiento puntuales. Esta distribución temporal, lejos de ser un detalle administrativo, refleja la naturaleza real del trabajo: la fase de implementación concentró la aplicación efectiva de los sprints, mientras que las fases inicial y final fueron más intensivas en documentación, revisión y cierre.

### 4.3.3 Artefactos del proceso de gestión

El proceso de gestión se apoya en tres artefactos definidos por Scrum. El Product Backlog es la lista ordenada y priorizada de todo el trabajo pendiente: los requisitos funcionales y no funcionales del sistema, las tareas de implementación de los pipelines de entrenamiento para arquitecturas CNN y Transformer, los módulos de generación de explicaciones XAI, los experimentos de benchmarking planificados y los documentos del TFG pendientes de elaboración. Es gestionado por el alumno y revisado de manera conjunta con el tutor en cada Sprint Planning. El Sprint Backlog es el subconjunto de elementos del Product Backlog seleccionados para el Sprint en curso, desglosados en tareas concretas y estimables que guían el trabajo durante el ciclo. El Increment es el conjunto de todos los elementos completados durante el Sprint, que deben cumplir la Definition of Done —el criterio acordado que define cuándo una tarea puede considerarse terminada— antes de ser presentados en el Sprint Review.

## 4.4 Seguimiento visual del trabajo con Kanban

Además del marco Scrum, se utiliza un tablero Kanban, gestionado a través de GitHub Projects, como instrumento visual para administrar el flujo de trabajo. La elección de GitHub Projects responde a que el repositorio del proyecto está alojado en GitHub, lo que permite asociar de manera directa las tareas del tablero a los commits, pull requests e issues del código, unificando toda la trazabilidad del desarrollo en una única plataforma.

El tablero se organiza en cuatro columnas que representan los estados por los que transita cada tarea: Por Hacer (To Do), para las tareas planificadas y aún no iniciadas; En Progreso (In Progress), para las tareas en desarrollo activo; En Revisión (In Review), para las tareas completadas por el alumno y pendientes de validación por el tutor; y Hecho (Done), para las tareas validadas que cumplen la Definition of Done.

La combinación de Scrum y Kanban, conocida en la literatura como Scrumban, permite aprovechar la estructura iterativa y los ritmos de inspección de Scrum junto con la visibilidad continua del flujo de trabajo que proporciona el tablero (Kniberg & Skarin, 2010; Reddy, 2016). El tablero Kanban aporta, por sí mismo, un mecanismo de gestión del flujo que ayuda a limitar el trabajo en curso y a detectar cuellos de botella (Anderson, 2010), algo especialmente valioso en un proyecto unipersonal en el que la capacidad de autogestión es fundamental.

## 4.5 Alcance de la metodología

El marco de gestión descrito en este capítulo se aplica exclusivamente al trabajo comprendido en este Plan de Proyecto, es decir, a la concepción, la implementación y la documentación de vitalXAI hasta su entrega. No gobierna, en cambio, las actividades que solo tendrían sentido si la plataforma pasara a explotarse de forma continuada —el mantenimiento del software, el soporte a usuarios, la actualización de los modelos o su despliegue en un centro sanitario—, que quedan fuera del alcance de un trabajo académico con un plazo de entrega fijado. La planificación tiene, por tanto, un horizonte claro: la finalización y la defensa de la memoria. Las posibles líneas de evolución futura de la plataforma se describen en la memoria como trabajo futuro, sin que ello amplíe el alcance de lo planificado ni comprometa la estimación de recursos de este documento. En la práctica, y de acuerdo con el calendario real descrito en el apartado 4.3.2, la metodología se aplicó de forma plena durante la fase de desarrollo activo, mientras que las fases inicial y final, más centradas en la planificación y en la documentación, se apoyaron en las reuniones de seguimiento y en el tablero Kanban más que en la cadencia formal de los sprints.

---

## Referencias del capítulo

Anderson, D. J. (2010). *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press.

Beck, K. (2000). *Extreme Programming Explained: Embrace Change*. Addison-Wesley.

Boehm, B., & Turner, R. (2004). *Balancing Agility and Discipline: A Guide for the Perplexed*. Addison-Wesley.

Dybå, T., & Dingsøyr, T. (2008). Empirical studies of agile software development: A systematic review. *Information and Software Technology*, 50(9-10), 833-859.

Kniberg, H., & Skarin, M. (2010). *Kanban and Scrum – Making the Most of Both*. C4Media.

Reddy, A. (2016). *The Scrumban [R]Evolution: Getting the Most Out of Agile, Scrum, and Lean Kanban*. Addison-Wesley.

Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game*.

Sutherland, J. (2014). *Scrum: The Art of Doing Twice the Work in Half the Time*. Crown Business.
