# Capítulo 16: Plan de pruebas

La verificación de la plataforma es una actividad transversal que acompaña a todo el ciclo de desarrollo y que permite comprobar, de forma sistemática y repetible, que el sistema construido se comporta conforme a lo especificado en el análisis. El plan de pruebas que se presenta en este capítulo recoge las verificaciones previstas para vitalXAI, de modo que se garantice el cumplimiento de los requisitos funcionales y no funcionales definidos en el capítulo 12: la corrección del comportamiento de cada componente, la interacción correcta entre los subsistemas, la protección de la plataforma frente a los vectores de ataque web más habituales, el rendimiento de las operaciones críticas y la integridad de los flujos completos de uso. Cada prueba se identifica mediante un código, describe el comportamiento que verifica, indica los subsistemas implicados y establece el criterio de éxito que debe satisfacerse para considerarse superada.

El desarrollo de vitalXAI ha seguido una metodología dirigida por pruebas (TDD, Test-Driven Development), de modo que la comprobación del comportamiento no es una actividad posterior a la implementación, sino un mecanismo de trabajo integrado en ella: cada capacidad funcional se ha desarrollado escribiendo primero la prueba que verifica su comportamiento esperado y, después, la implementación mínima que la hace superar. Esta metodología ha dado lugar a una batería de pruebas exhaustiva —más de ciento ochenta pruebas automatizadas distribuidas entre pruebas unitarias y de integración— que constituye la base sobre la que se asienta el plan de pruebas presentado a continuación. La automatización de la verificación, junto con su integración en el flujo de integración continua, garantiza que cualquier cambio posterior en el código pueda detectar regresiones de forma inmediata (Myers, Sandler & Badgett, 2011).

Las pruebas se organizan en cinco categorías, atendiendo al nivel de verificación que proporcionan y a la naturaleza de lo que comprueban: verificación de componentes individuales, verificación de los flujos entre subsistemas, pruebas de protección y control de acceso, pruebas de rendimiento y capacidad de respuesta y verificación integral de los flujos completos de uso. Las dos primeras categorías se corresponden con las pruebas unitarias y de integración ya implementadas en el proyecto; las tres restantes comprenden, junto con las verificaciones de seguridad ya automatizadas, el conjunto de pruebas de rendimiento, protección y sistema que el plan define para completar la estrategia de calidad de la plataforma. Las referencias a los ficheros de pruebas se indican en cada categoría, de modo que la correspondencia entre el plan y la implementación real de las pruebas quede documentada de forma inequívoca.

## 16.1 Verificación de componentes individuales

Las pruebas de esta categoría verifican el comportamiento correcto de los componentes del sistema de manera aislada, sin dependencia de la red, de la base de datos ni de servicios externos, que se sustituyen por dobles de prueba. Se centran en la lógica de negocio de mayor criticidad funcional y se organizan atendiendo a los subsistemas de análisis del capítulo 13, de modo que cada componente se verifica en el ámbito funcional en el que se utiliza. El conjunto comprende aproximadamente ciento ochenta y seis pruebas unitarias distribuidas en veinte ficheros bajo el directorio de pruebas unitarias del proyecto, y cubren la totalidad de los servicios y enrutadores del backend: la gestión de cuentas y sesiones, la validación de entradas, el motor de inferencia, la generación de explicaciones, la gestión del historial, el laboratorio de entrenamiento, la cola de trabajos, la internacionalización y la capa de acceso a datos.

### 16.1.1 Componentes del subsistema de acceso y gestión de cuentas

Las pruebas de este grupo verifican la autenticación y la gestión de la cuenta, así como la validación de las entradas del formulario de registro. Se comprueba que el registro crea la cuenta con la contraseña cifrada mediante un algoritmo de hash irrevers le, que el inicio de sesión con credenciales correctas genera una sesión válida y que las credenciales incorrectas son rechazadas sin generar sesión. También se verifican los tokens de acceso y de refresco: su creación, su verificación, la invalidación de los tokens revocados y el mecanismo de rotación, que detecta el robo de una sesión y revoca todos los tokens asociados. La tabla 38 recoge una muestra representativa de estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PU-001 | Verificar que el registro de usuario crea la cuenta con la contraseña cifrada. | `auth_service`, `auth_router` | El hash almacenado difiere de la contraseña original y es verificable mediante la función de verificación. |
| PU-002 | Verificar que el inicio de sesión con credenciales correctas genera una sesión válida. | `auth_router` | La sesión generada es válida y contiene el identificador del usuario. |
| PU-003 | Verificar que el inicio de sesión con credenciales incorrectas devuelve un error. | `auth_router` | El sistema rechaza el acceso sin generar sesión. |
| PU-004 | Verificar que un token de acceso caducado es rechazado. | `auth_service` | La verificación del token caducado devuelve sin identificar al usuario. |
| PU-005 | Verificar que la rotación del token de refresco invalida el anterior. | `auth_service` | El token antiguo deja de ser válido tras la rotación y el nuevo permite identificar al usuario. |
| PU-006 | Verificar que la detección de robo de sesión revoca todos los tokens del usuario. | `auth_service` | Tras el uso de un token revocado, todos los tokens asociados quedan invalidados. |
| PU-007 | Verificar que se rechaza un correo con formato no válido en el registro. | `input_validation` | El registro se rechaza indicando el campo erróneo y no se crea la cuenta. |
| PU-008 | Verificar que se rechaza una contraseña de menos de ocho caracteres. | `input_validation` | El registro se rechaza indicando el campo de contraseña. |
| PU-009 | Verificar que se rechaza un usuario duplicado. | `auth_router` | El registro devuelve un error de usuario existente y no crea la cuenta. |

*Tabla 38 - Verificación de componentes del subsistema de acceso y gestión de cuentas*

Los ficheros de pruebas que materializan estas verificaciones son `test_auth_service.py`, `test_auth_router.py` e `test_input_validation.py`, junto con `test_database.py`, que verifica la configuración del pool de conexiones, la lectura de credenciales desde el entorno y la creación de las tablas, y `test_rate_limiting.py`, que comprueba que el proceso de inicio de sesión está limitado a cinco peticiones por minuto.

### 16.1.2 Componentes del subsistema de diagnóstico asistido

Las pruebas de este grupo verifican el motor de inferencia y la generación de las explicaciones, que constituyen el núcleo clínico de la plataforma. Se comprueba que los modelos convolucionales se cargan correctamente desde sus pesos entrenados, que los modelos basados en atención se cargan desde su arquitectura de Hugging Face, que las predicciones producen las clases esperadas (PNEUMONIA o NORMAL), que los tamaños de entrada se ajustan a la arquitectura seleccionada y que el nivel de confianza se acota al intervalo válido. También se verifican los componentes de generación de los mapas de explicabilidad y de los informes PDF. La tabla 39 recoge una muestra representativa de estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PU-010 | Verificar que un modelo convolucional se carga desde sus pesos entrenados. | `ml_engine` | El modelo se carga y queda disponible para la inferencia. |
| PU-011 | Verificar que un modelo Transformer se carga desde su arquitectura preentrenada. | `ml_engine` | El modelo se carga con sus pesos y queda disponible para la inferencia. |
| PU-012 | Verificar que la predicción sobre una imagen con neumonía produce la clase PNEUMONIA. | `ml_engine` | El modelo clasifica la imagen en la clase PNEUMONIA. |
| PU-013 | Verificar que la predicción sobre una imagen sana produce la clase NORMAL. | `ml_engine` | El modelo clasifica la imagen en la clase NORMAL. |
| PU-014 | Verificar que la confianza de la predicción se acota al intervalo 0-100. | `ml_engine` | La confianza devuelta nunca sale del intervalo válido. |
| PU-015 | Verificar que se genera el mapa de explicabilidad para una arquitectura convolucional. | `xai_generator` | El mapa devuelto es una matriz normalizada de las dimensiones esperadas. |
| PU-016 | Verificar que se genera el mapa de atención para una arquitectura Transformer. | `xai_generator` | El mapa de atención se genera y normaliza correctamente. |
| PU-017 | Verificar que el informe PDF de una consulta se genera correctamente. | `pdf_generator` | La prueba devuelve la ruta del documento PDF generado. |

*Tabla 39 - Verificación de componentes del subsistema de diagnóstico asistido*

Los ficheros de pruebas que materializan estas verificaciones son `test_ml_engine.py`, `test_inference_router.py`, `test_xai_generator.py` y `test_pdf_generator.py`. Las pruebas del motor de inferencia emplean dobles de los modelos de TensorFlow para no depender de la carga real de los pesos durante la ejecución de la batería, en línea con la estrategia de aislamiento de las pruebas unitarias.

### 16.1.3 Componentes del subsistema de laboratorio MLOps

Las pruebas de este grupo constituyen el bloque más extenso de la verificación unitaria, dada la complejidad funcional del laboratorio. Verifican el asistente conversacional (la creación y reutilización de las sesiones de conversación, el manejo de los errores del servicio externo de Groq y la lectura de la clave de la API desde el entorno), el lanzamiento del entrenamiento (la construcción del dataset con sus etiquetas, la selección de la arquitectura, el cálculo del progreso y la actualización del estado en la base de datos), la gestión de las sesiones (consulta, renombrado, eliminación y verificación de propiedad) y la generación del informe PDF de la sesión. La tabla 40 recoge una muestra representativa de estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PU-018 | Verificar que una nueva conversación con el asistente crea la sesión de chat. | `trainer_router` | La conversación se inicia y la sesión queda registrada. |
| PU-019 | Verificar que una conversación existente reutiliza su histórico. | `trainer_router` | Los mensajes anteriores se conservan y se añade el nuevo mensaje. |
| PU-020 | Verificar el manejo del error cuando el servicio de Groq no responde. | `trainer_router` | El sistema devuelve un mensaje de error y no interrumpe el resto del flujo. |
| PU-021 | Verificar que el dataset de entrenamiento se construye con sus etiquetas. | `trainer_engine` | El dataframe contiene las imágenes y las etiquetas correspondientes. |
| PU-022 | Verificar que la selección de la arquitectura produce el modelo esperado. | `trainer_engine` | La arquitectura solicitada devuelve el objeto de modelo correspondiente. |
| PU-023 | Verificar que el cálculo del progreso del entrenamiento es correcto. | `trainer_engine` | El progreso calculado refleja la época actual respecto del total. |
| PU-024 | Verificar que un dataset ausente marca la sesión como fallida. | `trainer_engine` | La sesión pasa a estado fallido sin iniciar el entrenamiento. |
| PU-025 | Verificar que solo el propietario puede consultar una sesión. | `trainer_router`, `mlops_engine` | El acceso a una sesión ajena devuelve un error de autorización. |
| PU-026 | Verificar que solo el propietario puede eliminar una sesión. | `trainer_router` | La eliminación de una sesión ajena devuelve un error de autorización. |
| PU-027 | Verificar que el informe PDF de una sesión se genera correctamente. | `trainer_router` | La petición de informe de una sesión válida devuelve el documento PDF. |

*Tabla 40 - Verificación de componentes del subsistema de laboratorio MLOps*

Los ficheros de pruebas que materializan estas verificaciones son `test_trainer_router.py`, `test_trainer_engine.py` y `test_mlops_engine.py`. Este último incluye también las verificaciones de la lógica de selección de la carpeta del dataset y del aislamiento de la propiedad de las sesiones, que se comprueba en la práctica totalidad de las operaciones del laboratorio.

### 16.1.4 Componentes de los subsistemas de historial, administración y transversales

El grupo de historial verifica la consulta del listado de consultas, la visualización del detalle, el renombrado y la eliminación, comprobando en todos los casos que el sistema verifica la propiedad de la consulta y rechaza el acceso a consultas ajenas. El grupo de administración verifica el control de acceso basado en el rol de administrador para el listado de usuarios, la consulta de las consultas de un usuario y su detalle. Finalmente, el grupo transversal verifica la cola de trabajos (la consulta del estado, la cancelación de un trabajo pendiente y la gestión de la cancelación de un trabajo en ejecución según su interrumpibilidad), el worker de la cola (la reclamación de trabajos, la transición de estados y el manejo de cargas) y la internacionalización (los cuatro idiomas soportados, la selección del idioma desde la cookie y la recuperación de textos). La tabla 41 recoge una muestra representativa de estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PU-028 | Verificar que la consulta del historial devuelve solo las consultas del usuario. | `history_router` | El listado contiene únicamente las consultas propias. |
| PU-029 | Verificar que el acceso al detalle de una consulta ajena es denegado. | `history_router` | El sistema devuelve un error de autorización sin mostrar la información. |
| PU-030 | Verificar que el renombrado de una consulta ajena es denegado. | `history_router` | La operación devuelve un error de autorización y no modifica la consulta. |
| PU-031 | Verificar que el listado de usuarios requiere el rol de administrador. | `admin_router` | Un usuario sin rol de administración recibe un error 403. |
| PU-032 | Verificar que la consulta de las consultas de un usuario requiere el rol de administrador. | `admin_router` | Un usuario sin rol de administración recibe un error 403. |
| PU-033 | Verificar que se cancela un trabajo pendiente de la cola. | `queue_router` | El trabajo pendiente se cancela y deja de estar en la cola. |
| PU-034 | Verificar que la cancelación de un trabajo en ejecución se gestiona según su interrumpibilidad. | `queue_worker` | El sistema interrumpe el trabajo cuando resulta técnicamente posible y lo marca como cancelado; si no es interrumpible, informa de la limitación y no lo modifica. |
| PU-035 | Verificar que el worker rellama y procesa un trabajo de la cola. | `queue_worker` | El trabajo pasa a estado en ejecución y, al finalizar, a completado con su resultado. |
| PU-036 | Verificar la selección del idioma desde la cookie del navegador. | `lang` | La cookie selecciona el idioma correspondiente (es, en, zh o hi). |
| PU-037 | Verificar la recuperación de textos en el idioma solicitado. | `lang` | El texto devuelto corresponde al idioma seleccionado, con respaldo al español. |

*Tabla 41 - Verificación de componentes de los subsistemas de historial, administración y transversales*

Los ficheros de pruebas que materializan estas verificaciones son `test_history_router.py`, `test_admin_router.py`, `test_queue_router.py`, `test_queue_worker.py` y `test_lang.py`. Con esta cobertura, la totalidad de los subsistemas de análisis del capítulo 13 dispone de verificaciones unitarias sobre sus componentes de mayor criticidad.

## 16.2 Verificación de los flujos entre subsistemas

Las pruebas de esta categoría verifican el comportamiento del sistema cuando varios de sus subsistemas interactúan entre sí para completar un flujo funcional, superando el nivel de aislamiento de las pruebas unitarias. A diferencia de estas, que verifican cada componente por separado, las pruebas de integración ejercitan la colaboración entre las capas del sistema: la API, la capa de negocio y la base de datos, que se sustituye por una instancia en memoria durante la ejecución de las pruebas. El conjunto comprende las pruebas de integración implementadas bajo el directorio de pruebas de integración del proyecto, que cubren los flujos críticos de autenticación y de acceso, y se completan en el plan con las verificaciones de los flujos clínicos y de laboratorio previstas.

Las pruebas de integración implementadas verifican el flujo completo de acceso a la plataforma: el registro de un nuevo usuario, el inicio de sesión con las credenciales registradas, el acceso al panel y la verificación de que un usuario no autenticado es redirigido al punto de entrada. También se verifica que un usuario recién registrado no dispone de consultas en su historial. Estas pruebas confirman, de extremo a extremo entre la interfaz de la API y la base de datos, el comportamiento especificado en los casos de uso CU-001, CU-002 y CU-005. La tabla 42 recoge estas pruebas y las ampliaciones previstas.

| ID | Descripción | Componentes implicados | Criterio de éxito |
|---|---|---|---|
| PI-001 | Verificar el flujo completo de registro, inicio de sesión y acceso al panel. | SS-001, persistencia | El usuario se registra, inicia sesión con sus credenciales y accede al panel de diagnóstico. |
| PI-002 | Verificar que un usuario no autenticado es redirigido al punto de entrada. | SS-001 | El acceso a un recurso privado sin sesión redirige al inicio de sesión. |
| PI-003 | Verificar que un usuario recién registrado no tiene consultas en el historial. | SS-001, SS-003 | El historial del nuevo usuario se muestra vacío. |
| PI-004 | Verificar el flujo completo de un diagnóstico: subida, solicitud, encolado y resultado. | SS-002, SS-006, persistencia | La radiografía se sube, el diagnóstico se encola y el resultado queda registrado y accesible. |
| PI-005 | Verificar el aislamiento de datos entre dos usuarios. | SS-001, SS-003, SS-004 | Un usuario no puede acceder a las consultas ni a las sesiones del otro, obteniendo un error de autorización. |
| PI-006 | Verificar que el administrador puede supervisar las consultas de un usuario. | SS-001, SS-005 | El administrador consulta el detalle de una consulta de otro usuario sin restricciones de propiedad. |
| PI-007 | Verificar el flujo de lanzamiento de un experimento desde el asistente hasta la cola. | SS-004, SS-006, persistencia | La conversación completa los parámetros y el experimento se encola y ejecuta en segundo plano. |

*Tabla 42 - Verificación de los flujos entre subsistemas*

Las pruebas implementadas se encuentran en el fichero `test_auth_flow.py` del directorio de pruebas de integración. Las ampliaciones previstas (PI-004 a PI-007) cubren los flujos de extremo a extremo de mayor valor funcional de la plataforma: el diagnóstico asistido, el aislamiento de datos, la supervisión administrativa y el laboratorio de entrenamiento. Estas ampliaciones se ejecutan con la base de datos sustituida por una instancia en memoria y con los servicios externos —el modelo de Groq y los modelos de inferencia— simulados, de modo que la verificación se centra en la colaboración entre los subsistemas sin depender del entorno de producción.

## 16.3 Pruebas de protección y control de acceso

Las pruebas de esta categoría verifican que la plataforma aplica correctamente los mecanismos de protección especificados en los requisitos no funcionales de seguridad del capítulo 12 (RNF-001 a RNF-011). Se centran en los vectores de ataque más habituales sobre aplicaciones web autenticadas y en las cabeceras de seguridad que el sistema debe emitir en sus respuestas. Aunque el proyecto distingue la verificación de estos mecanismos como un nivel propio dentro del plan, las pruebas que los materializan están implementadas y se ejecutan como parte de la batería de pruebas del proyecto. La tabla 43 recoge una muestra representativa de estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PS-001 | Verificar que una petición POST sin token CSRF es rechazada. | `csrf_middleware` | El sistema devuelve un error 403 y no procesa la petición. |
| PS-002 | Verificar que una petición POST con token CSRF válido se procesa. | `csrf_middleware` | La petición se procesa correctamente. |
| PS-003 | Verificar que una petición POST con token CSRF erróneo es rechazada. | `csrf_middleware` | El sistema devuelve un error 403 y rechaza la petición. |
| PS-004 | Verificar que las peticiones GET están exentas de la protección CSRF. | `csrf_middleware` | Las peticiones GET se procesan sin exigir token CSRF. |
| PS-005 | Verificar que las respuestas incluyen la cabecera Content-Security-Policy. | `security_headers` | Todas las respuestas incluyen la cabecera con la política configurada. |
| PS-006 | Verificar que las respuestas incluyen la cabecera Strict-Transport-Security. | `security_headers` | La cabecera HSTS se incluye en todas las respuestas. |
| PS-007 | Verificar que las respuestas incluyen la cabecera X-Content-Type-Options. | `security_headers` | La cabecera se incluye para evitar la interpretación indebida de los tipos MIME. |
| PS-008 | Verificar que el inicio de sesión está limitado en frecuencia. | `rate_limiting` | La sexta petición de acceso en el mismo minuto es rechazada. |
| PS-009 | Verificar que el acceso con un token de refresco revocado es rechazado. | `auth_service` | El token revocado no permite renovar la sesión. |

*Tabla 43 - Pruebas de protección y control de acceso*

Los ficheros de pruebas que materializan estas verificaciones son `test_csrf_middleware.py`, `test_security_headers.py`, `test_rate_limiting.py` y las pruebas de gestión de tokens de `test_auth_service.py`. El plan prevé además una prueba de auditoría de la persistencia que inspeccione directamente las tablas de la base de datos para confirmar que el 100% de las contraseñas se almacena mediante hashes irreversibles y que ninguna entrada contiene texto plano, en línea con el requisito RNF-001 y con el registro de la actividad administrativa exigido por RNF-006.

## 16.4 Pruebas de rendimiento y capacidad de respuesta

Las pruebas de esta categoría verifican que la plataforma satisface los requisitos no funcionales de rendimiento y capacidad de respuesta definidos en el capítulo 12: el tiempo de respuesta de la inferencia (RNF-019), la ejecución sin bloqueo de la interfaz durante las tareas de larga duración (RNF-020) y la capacidad de acceso concurrente (RNF-021). A diferencia de las categorías anteriores, cuya implementación forma parte de la batería de pruebas automatizadas, estas verificaciones se definen en el plan como pruebas de rendimiento a ejecutar sobre el entorno de despliegue, de modo que sus criterios de éxito se miden sobre el sistema real y no sobre dobles de prueba. La tabla 44 recoge estas pruebas.

| ID | Descripción | Componente | Criterio de éxito |
|---|---|---|---|
| PR-001 | Verificar que la primera inferencia sobre una radiografía se completa en un tiempo razonable. | SS-002 | La primera consulta carga el modelo y produce el resultado en un tiempo que no hace incómodo el uso de la herramienta. |
| PR-002 | Verificar que las inferencias posteriores son casi instantáneas. | SS-002 | Las consultas siguientes sobre el mismo modelo se completan de forma sensiblemente más rápida que la primera, al reutilizar los pesos ya cargados. |
| PR-003 | Verificar que la interfaz permanece operativa durante una tarea de larga duración. | SS-004, SS-006 | Durante un entrenamiento o un análisis de explicabilidad, la plataforma continúa respondiendo a las peticiones del usuario sin bloquearse. |
| PR-004 | Verificar que el sistema soporta la carga de varios usuarios concurrentes. | Todos | Con un número razonable de usuarios concurrentes, el tiempo de respuesta no se degrada de forma significativa. |
| PR-005 | Verificar que el pool de conexiones gestiona el acceso concurrente a la base de datos. | persistencia | Las peticiones concurrentes se atienden sin errores de conexión ni contención excesiva. |

*Tabla 44 - Pruebas de rendimiento y capacidad de respuesta*

Las pruebas PR-001 y PR-002 se asocian directamente al requisito RNF-019, que exige que el sistema gestione la carga de los modelos de forma eficiente; la prueba PR-003 al requisito RNF-020, que exige que las tareas de larga duración se ejecuten de forma asíncrona sin bloquear la interfaz; y las pruebas PR-004 y PR-005 al requisito RNF-021, que exige la gestión del acceso concurrente mediante el pool de conexiones. Los umbrales concretos de tiempo para las pruebas PR-001 a PR-004 se fijan tras una primera campaña de medición sobre el entorno de despliegue, de modo que los criterios reflejen la infraestructura real de la plataforma.

## 16.5 Verificación integral de los flujos completos de uso

Las pruebas de esta categoría completan el plan de pruebas con la verificación integral de los flujos de uso de la plataforma, ejercitando la interacción del usuario con la interfaz a través de todos los subsistemas implicados, de manera análoga al uso real del sistema. Se definen en el plan como pruebas de sistema, dado que requieren el entorno de ejecución completo —la interfaz, la API, la capa de negocio, la base de datos y la cola de trabajos—, y se ejecutarán de forma manual o semiautomatizada sobre el despliegue de la plataforma. La tabla 45 recoge estas pruebas.

| ID | Descripción | Criterio de éxito |
|---|---|---|
| PE-001 | Verificar el flujo clínico completo: subida de una radiografía, selección del modelo, solicitud del diagnóstico, visualización del resultado, de los mapas de explicabilidad y generación del informe PDF. | El flujo completo se realiza sin errores y el profesional obtiene el diagnóstico, su confianza, los mapas de explicabilidad y el informe de la consulta. |
| PE-002 | Verificar la gestión del historial: consulta del listado, detalle de una consulta, renombrado y eliminación. | Todas las operaciones del historial se ejecutan correctamente y las consultas se recuperan tras cada operación. |
| PE-003 | Verificar el flujo del laboratorio: conversación con el asistente, lanzamiento del experimento, consulta de las sesiones y de los resultados, y generación del informe PDF. | El experimento se configura y lanza mediante el asistente, se ejecuta en segundo plano y sus resultados e informe se obtienen sin errores. |
| PE-004 | Verificar la ejecución asíncrona: consulta del estado de la cola y cancelación de un trabajo de la cola (pendiente o en ejecución cuando resulta interrumpible). | El usuario conoce el estado de sus trabajos y puede cancelar un trabajo pendiente o, cuando es posible, interrumpir uno en ejecución. |
| PE-005 | Verificar la supervisión administrativa: listado de usuarios, consulta de las consultas de un usuario y su detalle. | El administrador supervisa la actividad de un usuario concreto desde el panel de administración. |
| PE-006 | Verificar las capacidades transversales: cambio de idioma y del tema visual de la interfaz. | El idioma y el tema se aplican en toda la interfaz sin interrumpir la navegación. |

*Tabla 45 - Verificación integral de los flujos completos de uso*

El conjunto de las cinco categorías de pruebas presentadas en este capítulo constituye la estrategia de calidad de vitalXAI. Las pruebas unitarias y de integración, ya implementadas y automatizadas, proporcionan una verificación continua y repetible de la lógica de negocio y de los flujos críticos; las pruebas de protección verifican los mecanismos de seguridad especificados en el análisis; y las pruebas de rendimiento y de sistema completan la verificación sobre el entorno real de despliegue. Esta estrategia garantiza que el sistema construido satisface los requisitos funcionales y no funcionales del capítulo 12 y que las evoluciones futuras de la plataforma podrán incorporarse con un riesgo de regresión controlado y medible.

---

## Referencias del capítulo

Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software Testing* (3rd ed.). Wiley.
