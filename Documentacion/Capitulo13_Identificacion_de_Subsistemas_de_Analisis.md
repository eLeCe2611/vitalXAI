# Capítulo 13: Identificación de subsistemas de análisis

Una vez que el análisis ha fijado el ámbito del sistema (capítulo 11) y ha especificado en detalle sus requisitos y sus casos de uso (capítulo 12), el siguiente paso consiste en estructurar la plataforma en unidades de análisis que permitan abordar el diseño con orden. La descomposición del sistema en subsistemas de análisis persigue identificar las áreas funcionales que componen la plataforma y establecer de forma clara las responsabilidades de cada una antes de entrar en el diseño detallado. Cada subsistema agrupa un conjunto cohesionado de casos de uso y de requisitos funcionales que comparten una misma naturaleza, de modo que los límites entre subsistemas minimicen el acoplamiento entre áreas y maximicen la cohesión interna de cada una, dos propiedades que facilitan tanto el análisis posterior como la evolución del sistema (Larman, 2004).

Conviene precisar qué son y qué no son estos subsistemas. Los subsistemas identificados en este capítulo no son componentes de implementación ni deciden ninguna tecnología concreta: son unidades lógicas de análisis que servirán de base para la arquitectura del sistema y para el análisis de clases. La elección de las tecnologías que materializarán cada subsistema es una decisión que compete a la fase de diseño, que se aborda en capítulos posteriores de esta memoria. La descomposición que aquí se presenta se apoya directamente en los módulos funcionales declarados en la especificación de requisitos del capítulo 12, de forma que exista una correspondencia clara entre los subsistemas de análisis y las áreas funcionales ya definidas (Jacobson, Booch y Rumbaugh, 1999).

Cada subsistema se describe mediante una ficha normalizada en la que se recogen su identificador, su nombre, su descripción, los casos de uso y los requisitos funcionales que agrupa y los requisitos no funcionales que le resultan de aplicación. Esta forma de presentación permite verificar de un vistazo qué responsabilidades asume cada subsistema y qué exigencias del capítulo 12 sostienen su comportamiento. El sistema se descompone en los seis subsistemas de análisis siguientes: el subsistema de acceso y gestión de cuentas (SS-001), el subsistema de diagnóstico asistido (SS-002), el subsistema de gestión del historial de consultas (SS-003), el subsistema de laboratorio de experimentación MLOps (SS-004), el subsistema de supervisión y administración (SS-005) y el subsistema de capacidades transversales (SS-006). A continuación se describen uno a uno.

## 13.1 SS-001 — Subsistema de acceso y gestión de cuentas

Este subsistema es responsable de controlar el acceso a la plataforma y de gestionar la identidad de los usuarios registrados. Constituye la puerta de entrada al sistema, pues ninguna funcionalidad privada resulta accesible sin haber completado previamente el proceso de autenticación. Además del registro de nuevas cuentas y del inicio y cierre de sesión, este subsistema permite al usuario adaptar la interfaz a su idioma, una capacidad transversal que se gestiona desde la cuenta. Desde el punto de vista técnico, este subsistema garantiza que las contraseñas se almacenen de forma segura mediante técnicas de cifrado irreversible, que las sesiones se gestionen con las salvaguardas necesarias y que el acceso a las áreas privadas quede restringido a usuarios autenticados. Asimismo, establece la base lógica de identidad sobre la que se sustenta el aislamiento de datos entre usuarios (RF-005) y el control de roles (RF-006), dos requisitos de carácter transversal que condicionan el comportamiento del resto de los subsistemas.

| Campo | Contenido |
|---|---|
| ID | SS-001 |
| Nombre | Subsistema de Acceso y Gestión de Cuentas |
| Descripción | Este subsistema garantiza el registro de nuevos usuarios, el inicio y el cierre de sesión y la adaptación del idioma de la interfaz. Asegura que las contraseñas se almacenen mediante técnicas de cifrado irreversible, que la sesión se gestione de forma segura y que las áreas privadas queden restringidas a usuarios autenticados. Establece, además, la base lógica de identidad necesaria para el aislamiento transversal de datos entre usuarios y para el control de roles. |
| Casos de uso relacionados | CU-001, CU-002, CU-003, CU-004 |
| Requisitos funcionales relacionados | RF-001, RF-002, RF-003, RF-004, RF-005, RF-006 |
| Requisitos no funcionales relacionados | RNF-001, RNF-002, RNF-003, RNF-004, RNF-005, RNF-007, RNF-010, RNF-011, RNF-024 |

*Tabla 28 - SS-001: Subsistema de Acceso y Gestión de Cuentas*

## 13.2 SS-002 — Subsistema de diagnóstico asistido

Este subsistema agrupa la funcionalidad clínica de la plataforma: el flujo completo que permite al profesional sanitario obtener un diagnóstico asistido sobre una radiografía de tórax. Comprende el acceso al panel de diagnóstico, la subida de la imagen radiológica, la selección de la arquitectura de red neuronal con la que se desea realizar la inferencia, la solicitud del diagnóstico, la visualización del resultado con su nivel de confianza y la visualización de los mapas de explicabilidad que justifican la decisión del modelo. Por manejar datos sanitarios, este subsistema queda sometido a los requisitos de confidencialidad y protección de datos del Reglamento General de Protección de Datos, a la anonimización de los conjuntos de datos y a la exclusión de cualquier dato personal identificable. Asimismo, la solicitud del diagnóstico se ejecuta de forma asíncrona, de modo que la interfaz no se bloquea durante la inferencia y el tiempo de respuesta se mantiene dentro de los límites exigidos.

| Campo | Contenido |
|---|---|
| ID | SS-002 |
| Nombre | Subsistema de Diagnóstico Asistido |
| Descripción | Este subsistema cubre el flujo clínico de la plataforma: acceso al panel de diagnóstico, subida de una radiografía de tórax, selección de la arquitectura del modelo, solicitud asíncrona del diagnóstico, visualización del resultado con su confianza, visualización de los mapas de explicabilidad y generación del informe PDF de la consulta. Su comportamiento queda sujeto a los requisitos de confidencialidad y protección de datos, así como a los de rendimiento de la inferencia y de ejecución sin bloqueo de la interfaz. |
| Casos de uso relacionados | CU-005, CU-006, CU-007, CU-008, CU-009, CU-010, CU-037 |
| Requisitos funcionales relacionados | RF-007, RF-008, RF-009, RF-010, RF-011, RF-012, RF-039 |
| Requisitos no funcionales relacionados | RNF-008, RNF-012, RNF-013, RNF-014, RNF-015, RNF-019, RNF-020 |

*Tabla 29 - SS-002: Subsistema de Diagnóstico Asistido*

## 13.3 SS-003 — Subsistema de gestión del historial de consultas

Este subsistema es el encargado de conservar y gestionar el historial de consultas de diagnóstico de cada usuario autenticado. Permite consultar el listado de las consultas realizadas, visualizar el detalle completo de una consulta anterior —incluidos la imagen, el resultado, la confianza y los metadatos asociados—, renombrar una consulta para organizarla según la preferencia del usuario y eliminar aquellas consultas que ya no se deseen conservar. Al operar sobre registros de diagnóstico con datos sanitarios, este subsistema comparte con el de diagnóstico asistido los requisitos de confidencialidad y protección de datos, y añade los requisitos de integridad y durabilidad de la persistencia, que garantizan que el historial se conserva de forma fiable a lo largo del tiempo y que cada consulta queda correctamente asociada a su propietario, en línea con el aislamiento de datos entre usuarios (RF-005).

| Campo | Contenido |
|---|---|
| ID | SS-003 |
| Nombre | Subsistema de Gestión del Historial de Consultas |
| Descripción | Este subsistema gestiona el historial de consultas de diagnóstico del usuario autenticado: la consulta del listado de consultas, la visualización del detalle de una consulta anterior, el renombrado y la eliminación de consultas. Preserva la confidencialidad de los datos sanitarios y la integridad y durabilidad de la persistencia del historial. |
| Casos de uso relacionados | CU-011, CU-012, CU-013, CU-014 |
| Requisitos funcionales relacionados | RF-013, RF-014, RF-015, RF-016 |
| Requisitos no funcionales relacionados | RNF-012, RNF-013, RNF-014, RNF-016, RNF-031 |

*Tabla 30 - SS-003: Subsistema de Gestión del Historial de Consultas*

## 13.4 SS-004 — Subsistema de laboratorio de experimentación MLOps

Este subsistema constituye el segundo núcleo funcional de la plataforma y agrupa la experimentación MLOps: el asistente conversacional que configura los experimentos, la selección de la carpeta del dataset, el lanzamiento asíncrono de los entrenamientos, la gestión de las sesiones de experimentación y la consulta de sus resultados. Dentro de una sesión, este subsistema cubre la consulta de los resultados de cada modelo, la visualización de sus mapas de explicabilidad, el ranking de modelos, la comparativa estadística con su recálculo, la validación externa sobre datos independientes y la generación del informe PDF. Su naturaleza asíncrona lo vincula directamente al mecanismo de cola de trabajos, de modo que los entrenamientos de larga duración se ejecutan sin bloquear la interfaz y sus resultados quedan disponibles cuando finalizan. Por tratarse del área donde se entrenan y comparan los modelos, este subsistema incorpora los requisitos de reproducibilidad de los experimentos y del entorno de ejecución, junto con los de concurrencia, robustez y disponibilidad del servicio durante las tareas de larga duración.

| Campo | Contenido |
|---|---|
| ID | SS-004 |
| Nombre | Subsistema de Laboratorio de Experimentación MLOps |
| Descripción | Este subsistema cubre la experimentación MLOps de la plataforma: la configuración de experimentos mediante el asistente conversacional, la selección del dataset, el lanzamiento asíncrono de los entrenamientos con la limitación de entrenamientos simultáneos, la gestión de las sesiones y la consulta de resultados, mapas de explicabilidad, ranking, comparativa estadística, validación externa e informes PDF. Depende de la ejecución asíncrona de tareas y aplica los requisitos de reproducibilidad, concurrencia y robustez. |
| Casos de uso relacionados | CU-015, CU-016, CU-017, CU-018, CU-019, CU-020, CU-021, CU-022, CU-023, CU-024, CU-025, CU-026, CU-027, CU-028, CU-029, CU-030, CU-039 |
| Requisitos funcionales relacionados | RF-017, RF-018, RF-019, RF-020, RF-021, RF-022, RF-023, RF-024, RF-025, RF-026, RF-027, RF-028, RF-029, RF-030, RF-031, RF-032, RF-041 |
| Requisitos no funcionales relacionados | RNF-012, RNF-020, RNF-021, RNF-022, RNF-027, RNF-028, RNF-029, RNF-030, RNF-033, RNF-034 |

*Tabla 31 - SS-004: Subsistema de Laboratorio de Experimentación MLOps*

## 13.5 SS-005 — Subsistema de supervisión y administración de la plataforma

Este subsistema agrupa las operaciones de gobierno de la plataforma, restringidas al rol de administrador. Permite consultar el listado de usuarios registrados, examinar el historial de consultas de diagnóstico de un usuario concreto y visualizar el detalle completo de una consulta, incluidos la imagen, el resultado, la confianza y los metadatos asociados. Su propósito es proporcionar al administrador una visión global del uso que se hace de la plataforma y los medios para auditar cualquier incidencia ante la que deba intervenir. Por supervisar datos personales y de diagnóstico de terceros, este subsistema queda sometido a los requisitos de protección de datos y al requisito de auditoría de la actividad administrativa, que garantiza la trazabilidad de las acciones de supervisión. El control de roles (RF-006) delimita estrictamente quién puede invocar estas operaciones, de modo que solo el administrador accede a ellas.

| Campo | Contenido |
|---|---|
| ID | SS-005 |
| Nombre | Subsistema de Supervisión y Administración de la Plataforma |
| Descripción | Este subsistema agrupa las operaciones de administración restringidas al rol de administrador: la consulta del listado de usuarios, la consulta de las consultas de diagnóstico de un usuario, la visualización del detalle de una consulta y la gestión de las cuentas de usuario (desactivar, cambiar rol o eliminar). Aplica los requisitos de protección de datos, de auditoría de la actividad administrativa y de registro de eventos de seguridad. |
| Casos de uso relacionados | CU-031, CU-032, CU-033, CU-038 |
| Requisitos funcionales relacionados | RF-033, RF-034, RF-035, RF-040 |
| Requisitos no funcionales relacionados | RNF-006, RNF-009, RNF-012 |

*Tabla 32 - SS-005: Subsistema de Supervisión y Administración de la Plataforma*

## 13.6 SS-006 — Subsistema de capacidades transversales de la plataforma

Este subsistema reúne las capacidades que no pertenecen a un ámbito funcional concreto, sino que afectan a toda la plataforma. Por un lado, gestiona la cola de trabajos asíncronos, que cubre los diagnósticos, los entrenamientos y las validaciones externas: permite consultar el estado de cada trabajo —pendiente, en ejecución, completado o fallido— y cancelar un trabajo de la cola, esté pendiente o, cuando resulte técnicamente posible, en ejecución. Al ser el mecanismo compartido de ejecución asíncrona, este subsistema integra los requisitos de robustez y disponibilidad que garantizan que las tareas de larga duración no degradan el servicio, que los errores de un trabajo se gestionan de forma aislada y que los trabajos se recuperan tras un reinicio del servidor. Por otro lado, este subsistema cubre las capacidades de interfaz de carácter transversal, como la personalización del tema visual, y aplica los requisitos de usabilidad, multilingüismo y accesibilidad de la interfaz.

| Campo | Contenido |
|---|---|
| ID | SS-006 |
| Nombre | Subsistema de Capacidades Transversales de la Plataforma |
| Descripción | Este subsistema agrupa las capacidades transversales de la plataforma: la consulta del estado de la cola de trabajos asíncronos, la cancelación de los trabajos de la cola y la personalización del tema visual de la interfaz. Integra los requisitos de robustez y disponibilidad del servicio durante las tareas de larga duración, así como los de usabilidad, multilingüismo y accesibilidad de la interfaz. |
| Casos de uso relacionados | CU-034, CU-035, CU-036 |
| Requisitos funcionales relacionados | RF-036, RF-037, RF-038 |
| Requisitos no funcionales relacionados | RNF-023, RNF-024, RNF-025, RNF-026, RNF-027, RNF-028, RNF-029, RNF-030 |

*Tabla 33 - SS-006: Subsistema de Capacidades Transversales de la Plataforma*

## 13.7 Síntesis de la descomposición en subsistemas

La descomposición presentada en este capítulo recoge, en los seis subsistemas descritos, la totalidad de las capacidades de la plataforma declaradas en el capítulo 12: los treinta y nueve casos de uso y los cuarenta y un requisitos funcionales quedan distribuidos entre los subsistemas, de modo que cada caso de uso pertenece exactamente a un subsistema y cada requisito funcional queda asignado al subsistema que lo materializa. Los dos requisitos de carácter transversal —el aislamiento de datos entre usuarios (RF-005) y el control de roles (RF-006)— se declaran formalmente en el subsistema de acceso y gestión de cuentas, que establece la identidad y la sesión sobre las que ambos se aplican, pero condicionan el comportamiento de todos los demás subsistemas, como se ha señalado en las fichas.

Conviene destacar las dos dependencias principales que se desprenden de esta descomposición. En primer lugar, los subsistemas de diagnóstico asistido (SS-002), de laboratorio de experimentación (SS-004) y de supervisión y administración (SS-005) presuponen que el usuario se ha autenticado a través del subsistema de acceso (SS-001) y que, por tanto, existe una identidad sobre la que aplicar el aislamiento de datos y el control de roles. En segundo lugar, los subsistemas SS-002 y SS-004 delegan la ejecución de sus tareas de larga duración en el mecanismo de cola de trabajos del subsistema de capacidades transversales (SS-006), que actúa como servicio común de ejecución asíncrona.

Estos subsistemas de análisis constituyen la unidad de trabajo sobre la que se apoyarán las etapas siguientes de la memoria: el análisis de clases, que identificará las entidades del dominio y sus responsabilidades, y el diseño del sistema, que tomará las decisiones tecnológicas que materializarán cada subsistema. La correspondencia entre los subsistemas de análisis, los módulos funcionales de requisitos y los módulos de casos de uso garantiza que ninguna capacidad declarada en la especificación de requisitos quede sin representación en el análisis, de forma coherente con el enfoque dirigido por requisitos que guía este proyecto (Larman, 2004).

---

## Referencias del capítulo

Jacobson, I., Booch, G., & Rumbaugh, J. (1999). *The Unified Software Development Process*. Addison-Wesley.

Larman, C. (2004). *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3rd ed.). Prentice Hall.