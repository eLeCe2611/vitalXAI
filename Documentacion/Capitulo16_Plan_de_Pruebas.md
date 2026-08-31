# Capítulo 16: Plan de pruebas

Este capítulo define las comprobaciones previstas para evaluar si vitalXAI se comporta conforme a los requisitos del capítulo 12. El plan establece qué se comprueba, qué resultado permitiría considerar superada cada prueba y qué requisitos se relacionan con ella. No documenta ejecuciones ni resultados. Esa información se conserva en los capítulos 33 a 36, mientras que el capítulo 25 define los entornos y niveles de verificación.

La planificación distingue entre pruebas de componentes, pruebas de integración, pruebas de protección, pruebas de rendimiento y pruebas de sistema. Cada prueba recibe un identificador estable para relacionarla con los requisitos, los casos de uso y los resultados que se documenten posteriormente. Los criterios se formulan sobre el comportamiento observable y no sobre los nombres de los ficheros o la organización interna del repositorio (Myers, Sandler, & Badgett, 2011). Los identificadores del plan agrupan el alcance previsto de las comprobaciones; no implican que exista un test con el mismo nombre en el repositorio.

## 16.1 Pruebas de componentes individuales

Estas pruebas comprueban unidades funcionales de forma aislada. Las dependencias externas se sustituyen por dobles de prueba y se incluyen tanto los caminos normales como las principales condiciones de error, siguiendo el alcance previsto para las pruebas unitarias (Myers, Sandler, & Badgett, 2011).

| Identificadores | Ámbito | Criterio general |
|---|---|---|
| PU-001 a PU-009 | Registro, autenticación, sesiones, validación de entradas y usuarios duplicados. | Las entradas válidas producen el resultado esperado y las inválidas o no autorizadas son rechazadas sin efectos indebidos. |
| PU-010 a PU-017 | Inferencia, confianza, mapas de explicabilidad e informes del diagnóstico. | El sistema produce una predicción válida, los artefactos esperados y un informe accesible cuando los datos son correctos. |
| PU-018 a PU-027 | Asistente, configuración, entrenamiento, sesiones y resultados del laboratorio. | Las operaciones del laboratorio conservan la configuración, actualizan los estados correctos y respetan la propiedad del usuario. |
| PU-028 a PU-030 | Consulta, detalle, renombrado y propiedad del historial. | El usuario solo consulta o modifica sus propias consultas y las operaciones válidas actualizan el historial correctamente. |
| PU-031 a PU-032 | Operaciones de supervisión administrativa. | Las operaciones reservadas al administrador rechazan a los usuarios sin el rol requerido. |
| PU-033 a PU-035 | Consulta, cancelación y procesamiento de trabajos. | Los trabajos cambian de estado conforme al flujo previsto y solo pueden cancelarse mientras permanecen pendientes. |
| PU-036 a PU-037 | Internacionalización de la interfaz. | El idioma seleccionado se aplica correctamente y se utiliza el idioma de respaldo cuando falta una traducción. |

## 16.2 Pruebas de los flujos entre subsistemas

Estas pruebas comprueban la colaboración entre varias partes del sistema. Su objetivo es comprobar que una operación iniciada por el usuario atraviesa correctamente la autenticación, la lógica de aplicación, la persistencia y, cuando corresponde, la cola de trabajos (Myers, Sandler, & Badgett, 2011).

| Identificador | Flujo | Criterio de éxito |
|---|---|---|
| PI-001 | Registro, inicio de sesión y acceso al panel. | El usuario se registra, inicia sesión y accede al área privada. |
| PI-002 | Acceso privado sin sesión. | El sistema rechaza o redirige al usuario no autenticado. |
| PI-003 | Historial de un usuario recién registrado. | El historial inicial aparece vacío para el usuario recién registrado. |
| PI-004 | Diagnóstico completo desde la carga hasta el resultado. | La imagen se valida, el trabajo se encola y el resultado queda disponible. |
| PI-005 | Aislamiento de datos entre usuarios. | Un usuario no puede consultar ni modificar consultas o sesiones ajenas. |
| PI-006 | Supervisión administrativa. | El administrador puede consultar la información permitida y un usuario ordinario no puede hacerlo. |
| PI-007 | Laboratorio desde la configuración hasta la cola. | La configuración válida crea la sesión y el trabajo se encola para su procesamiento. |

## 16.3 Pruebas de protección y control de acceso

Estas pruebas comprueban los requisitos de seguridad del capítulo 12 mediante escenarios controlados y comprobaciones de las respuestas del sistema. El catálogo de amenazas de OWASP constituye el marco de referencia de los controles de seguridad del proyecto (OWASP, 2024).

| Identificador | Protección | Criterio de éxito |
|---|---|---|
| PS-001 a PS-004 | Protección frente a falsificación de peticiones. | Las peticiones que modifican el estado requieren un token válido y las peticiones fraudulentas son rechazadas. |
| PS-005 a PS-007 | Cabeceras de seguridad. | Las respuestas incluyen las protecciones exigidas por el requisito correspondiente. |
| PS-008 | Limitación de peticiones de acceso. | Tras cinco peticiones fallidas desde una misma dirección en un minuto, la siguiente petición de acceso debe rechazarse y el bloqueo debe mantenerse durante el intervalo definido. |
| PS-009 | Tokens de sesión revocados. | Una credencial de refresco revocada no permite renovar la sesión. |

Los requisitos de auditoría y registro de eventos de seguridad, así como los controles de protección de datos pendientes, se mantienen identificados en la matriz de trazabilidad como comprobaciones que requieren una prueba específica antes de poder declararse verificados.

## 16.4 Pruebas de rendimiento y capacidad de respuesta

Estas pruebas se ejecutan sobre el entorno de sistema definido en el capítulo 25. Sus criterios proceden directamente de los requisitos del capítulo 12.

| Identificador | Requisito | Criterio de éxito |
|---|---|---|
| PR-001 | RNF-019 | El identificador del trabajo se devuelve en menos de 2 segundos. |
| PR-002 | RNF-019 | La inferencia con el modelo ya cargado finaliza en menos de 15 segundos. |
| PR-003 | RNF-020 | La interfaz continúa respondiendo durante una tarea de larga duración. |
| PR-004 | RNF-021 | Diez usuarios autenticados realizan operaciones concurrentes sin superar el doble del tiempo de carga baja y preservando el aislamiento. |
| PR-005 | RNF-021 | Las operaciones concurrentes se atienden sin errores de conexión. |

## 16.5 Pruebas de sistema y validación funcional

Estas pruebas comprueban los flujos completos desde la interfaz y sobre el entorno de sistema. Incluyen los escenarios principales de uso y las operaciones que atraviesan varios subsistemas.

| Identificador | Flujo | Criterio de éxito |
|---|---|---|
| PE-001 | Diagnóstico completo, incluidos resultado, explicabilidad e informe. | El profesional completa el flujo y obtiene todos los artefactos previstos. |
| PE-002 | Gestión del historial. | El usuario consulta, visualiza, renombra y elimina sus consultas correctamente. |
| PE-003 | Laboratorio MLOps. | El usuario configura y lanza un experimento y puede consultar sus resultados e informe. |
| PE-004 | Cola de trabajos. | El usuario consulta el estado y cancela trabajos conforme a las condiciones permitidas. |
| PE-005 | Supervisión administrativa. | El administrador consulta usuarios y consultas conforme a sus permisos. |
| PE-006 | Idioma y tema visual. | Las preferencias se aplican sin perder el estado de navegación. |

## 16.6 Matriz de trazabilidad entre requisitos y pruebas

La matriz relaciona los requisitos con las pruebas previstas para aportar evidencia sobre su comportamiento. Una relación en esta tabla no demuestra que la prueba se haya ejecutado ni que el requisito esté verificado. Una celda vacía o una observación de pendiente indica que el plan no define una comprobación suficiente para declararlo verificado.

| Requisitos | Pruebas relacionadas | Alcance de la comprobación |
|---|---|---|
| RF-001 a RF-006 | PU-001 a PU-009, PI-001 a PI-003, PS-008 y PS-009 | Cuenta, acceso, sesión, validación, propiedad y control de acceso. |
| RF-007 a RF-012 | PU-010 a PU-016, PI-004 y PE-001 | Flujo de diagnóstico, resultado y explicabilidad. |
| RF-013 a RF-016 | PU-028 a PU-030, PI-003, PI-005 y PE-002 | Consulta y gestión del historial propio. |
| RF-017 a RF-032 | PU-018 a PU-027, PI-007 y PE-003 | Configuración, entrenamiento, resultados, comparación y validación del laboratorio. |
| RF-033 a RF-035 | PU-031 y PU-032, PI-006 y PE-005 | Supervisión administrativa y restricciones de rol. |
| RF-036 a RF-038 | PU-033 a PU-037, PE-004 y PE-006 | Cola de trabajos, cancelación e internacionalización. La cancelación prevista se limita a trabajos pendientes. |
| RF-039 | PU-017 y PE-001 | Informe PDF individual del diagnóstico. |
| RF-040 | PI-006 y PE-005 | Gestión de cuentas por el administrador, prevista para cuando esta capacidad esté implementada; no existe evidencia actual de ejecución. |
| RF-041 | PI-007 y PE-003 | Limitación de entrenamientos simultáneos y encolados, prevista para cuando esta capacidad esté implementada; no existe evidencia actual de ejecución. |
| RNF-001 a RNF-005, RNF-007, RNF-008, RNF-010 y RNF-011 | PU-001, PU-007 a PU-009, PS-001 a PS-009 | Protección de credenciales, ficheros, entradas, peticiones, respuestas y sesiones. La cobertura de cada requisito debe confirmarse en los resultados específicos. |
| RNF-006 y RNF-009 | Pendiente de prueba específica | Auditoría administrativa y registro de eventos de seguridad. |
| RNF-012 a RNF-018 | PI-004 a PI-007 y PE-001 a PE-005 | Comprobaciones previstas sobre protección y tratamiento de datos en los flujos que los utilizan. La cobertura normativa completa y la evidencia de ejecución requieren revisión específica. |
| RNF-019 a RNF-022 | PR-001 a PR-005, PI-004, PI-007 y PE-003 | Rendimiento, ejecución asíncrona, concurrencia y comportamiento con recursos ocupados. |
| RNF-023 a RNF-026 | PU-036 a PU-037 y PE-006 | Comprobaciones previstas sobre idioma, uso, presentación y accesibilidad. La usabilidad no se valida con usuarios reales y la evidencia de todos los criterios requiere revisión específica. |
| RNF-027 a RNF-030 | PU-033 a PU-035, PR-003, PE-003 y PE-004 | Disponibilidad, errores, recuperación y aislamiento de fallos en trabajos. |
| RNF-031 y RNF-032 | PU-018 a PU-027 y PE-002 a PE-003 | Integridad, persistencia y recuperación de la información. |
| RNF-033 y RNF-034 | PU-018 a PU-027 y PE-003 | Reproducibilidad de experimentos y del entorno de ejecución. |
| RNF-035 a RNF-038 | No aplica como prueba de sistema | Compromisos del proceso y entregables del proyecto. Se prevé verificarlos mediante revisión documental y de calidad. |

La matriz permite localizar qué comprobaciones previstas deben contrastarse en los capítulos 33 a 36. También deja visibles las áreas sin prueba específica y evita afirmar que una relación documental equivale a una verificación superada. Los resultados de cada prueba, los recuentos y la cobertura real se documentan únicamente en la parte de verificación.
