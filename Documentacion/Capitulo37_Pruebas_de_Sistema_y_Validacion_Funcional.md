# Capítulo 37: Pruebas de sistema y validación funcional

Las pruebas de sistema completan la verificación de vitalXAI con la comprobación integral de los flujos de uso de la plataforma, ejercitando la interacción del usuario con la interfaz a través de todos los subsistemas implicados, de manera análoga al uso real del sistema. Este capítulo describe las pruebas de sistema del plan de pruebas del capítulo 16 —los códigos PE-001 a PE-006—, presentando cada flujo completo con sus pasos, su criterio de éxito y el resultado de su verificación. Las pruebas se ejecutan manualmente sobre el despliegue real de la plataforma, con el entorno de sistema de la estrategia de verificación del capítulo 25, y cada flujo se documenta con una captura de pantalla real del sistema en funcionamiento, insertada en la ilustración correspondiente.

Las pruebas de sistema verifican los seis flujos completos de la plataforma: el flujo clínico del diagnóstico, la gestión del historial, el flujo del laboratorio de entrenamiento, la ejecución asíncrona de la cola, la supervisión administrativa y las capacidades transversales de idioma y tema. Cada prueba recorre las operaciones del flujo sobre la interfaz real, desde el registro o el acceso hasta la obtención del resultado, y comprueba que el comportamiento coincide con el especificado en los casos de uso del análisis. La ejecución de cada prueba se apoya en la documentación de operación de la plataforma y en las cuentas de acceso del entorno de despliegue.

## 37.1 PE-001: Flujo clínico completo

La prueba PE-001 verifica el flujo clínico completo del diagnóstico asistido: la subida de una radiografía, la selección del modelo, la solicitud del diagnóstico, la visualización del resultado y de los mapas de explicabilidad, y la generación del informe PDF. La prueba se inicia desde el panel de diagnóstico del usuario autenticado y recorre las operaciones descritas en los casos de uso CU-005 a CU-010 y CU-037. Los pasos de la prueba son los siguientes.

1. El usuario autenticado accede al panel de diagnóstico.
2. El usuario sube una radiografía de tórax en la zona de carga.
3. El usuario selecciona una arquitectura de inteligencia artificial.
4. El usuario solicita el diagnóstico y espera el procesamiento en la cola.
5. El sistema muestra el resultado con la etiqueta, la confianza y el modelo empleado.
6. El usuario visualiza los mapas de explicabilidad y el informe PDF de la consulta.

El criterio de éxito de la prueba es que el flujo completo se realiza sin errores y el profesional obtiene el diagnóstico, su confianza, los mapas de explicabilidad y el informe de la consulta. El resultado esperado se confirma con la captura del panel de diagnóstico mostrando el resultado y los artefactos generados.

*Ilustración 1 - Flujo de diagnóstico completado con resultado, mapas de explicabilidad e informe*

## 37.2 PE-002: Gestión del historial

La prueba PE-002 verifica la gestión del historial de consultas: la consulta del listado, el detalle de una consulta, el renombrado y la eliminación. La prueba se realiza desde el panel de diagnóstico, sobre las consultas del usuario, y recorre las operaciones descritas en los casos de uso CU-011 a CU-014. Los pasos de la prueba son los siguientes.

1. El usuario consulta su historial de consultas en el panel.
2. El usuario abre el detalle de una consulta del listado.
3. El usuario renombra la consulta con un nuevo nombre visible.
4. El usuario elimina una consulta, confirmando la operación.

El criterio de éxito de la prueba es que todas las operaciones del historial se ejecutan correctamente y las consultas se recuperan tras cada operación, con el aislamiento de datos entre usuarios respetado. El resultado esperado se confirma con la captura del historial y del detalle de una consulta.

*Ilustración 2 - Historial de consultas con su detalle*

## 37.3 PE-003: Flujo del laboratorio

La prueba PE-003 verifica el flujo del laboratorio de entrenamiento: la conversación con el asistente, el lanzamiento del experimento, la consulta de las sesiones y de los resultados, y la generación del informe PDF de la sesión. La prueba se realiza desde el laboratorio del usuario investigador y recorre las operaciones descritas en los casos de uso CU-015 a CU-030. Los pasos de la prueba son los siguientes.

1. El usuario accede al laboratorio de entrenamiento.
2. El usuario configura el experimento con el asistente conversacional y selecciona la carpeta del dataset.
3. El usuario lanza el experimento y lo encola en segundo plano.
4. El usuario consulta la sesión, el ranking de modelos y los resultados de un modelo.
5. El usuario genera el informe PDF de la sesión.

El criterio de éxito de la prueba es que el experimento se configura y lanza mediante el asistente, se ejecuta en segundo plano y sus resultados e informe se obtienen sin errores. El resultado esperado se confirma con la captura de la vista de resultados de la sesión.

*Ilustración 3 - Laboratorio de entrenamiento con la vista de resultados de la sesión*

## 37.4 PE-004: Ejecución asíncrona de la cola

La prueba PE-004 verifica la ejecución asíncrona de la cola de trabajos: la consulta del estado de la cola y la cancelación de un trabajo pendiente. La prueba se realiza desde el panel de diagnóstico o el laboratorio, y recorre las operaciones descritas en los casos de uso CU-034 y CU-035. Los pasos de la prueba son los siguientes.

1. El usuario consulta el panel de la cola de trabajos.
2. El usuario comprueba el estado de sus trabajos (encolado, en ejecución, completado o fallido).
3. El usuario cancela un trabajo pendiente, confirmando la operación.

El criterio de éxito de la prueba es que el usuario conoce el estado de sus trabajos y puede cancelar un trabajo pendiente, mientras que un trabajo en ejecución no se interrumpe. El resultado esperado se confirma con la captura del panel de la cola de trabajos.

*Ilustración 4 - Panel de la cola de trabajos con su estado*

## 37.5 PE-005: Supervisión administrativa

La prueba PE-005 verifica la supervisión administrativa de la plataforma: el listado de usuarios, la consulta de las consultas de un usuario y su detalle. La prueba se realiza desde el panel del usuario con rol de administrador, y recorre las operaciones descritas en los casos de uso CU-031 a CU-033. Los pasos de la prueba son los siguientes.

1. El administrador abre el panel de administración desde su ventana.
2. El administrador consulta el listado de usuarios con sus recuentos de actividad.
3. El administrador consulta las consultas de un usuario concreto y el detalle de una consulta.

El criterio de éxito de la prueba es que el administrador supervisa la actividad de un usuario concreto desde el panel de administración, con la comprobación de rol aplicada por el sistema. El resultado esperado se confirma con la captura del diálogo de administración.

*Ilustración 5 - Supervisión administrativa de la actividad de un usuario*

## 37.6 PE-006: Capacidades transversales

La prueba PE-006 verifica las capacidades transversales de la plataforma: el cambio de idioma y el cambio del tema visual de la interfaz. La prueba se realiza desde cualquiera de las ventanas del sistema y recorre las operaciones descritas en los casos de uso CU-004 y CU-036. Los pasos de la prueba son los siguientes.

1. El usuario cambia el idioma de la interfaz mediante el selector de idioma.
2. El sistema aplica las traducciones en toda la interfaz sin recargar la página.
3. El usuario alterna el tema visual entre el claro y el oscuro.
4. El sistema aplica el tema en toda la interfaz y conserva la preferencia.

El criterio de éxito de la prueba es que el idioma y el tema se aplican en toda la interfaz sin interrumpir la navegación. El resultado esperado se confirma con la captura de una ventana en el idioma y el tema seleccionados.

*Ilustración 6 - Interfaz de la plataforma con el idioma y el tema seleccionados*

## 37.7 Resultados de la validación funcional

Las seis pruebas de sistema verifican los flujos completos de uso de la plataforma sobre el despliegue real, cubriendo el diagnóstico, el historial, el laboratorio, la cola, la administración y las capacidades transversales. La tabla siguiente resume el resultado de la validación funcional.

| ID | Flujo verificado | Resultado |
|---|---|---|
| PE-001 | Flujo clínico completo del diagnóstico | Superada. |
| PE-002 | Gestión del historial de consultas | Superada. |
| PE-003 | Flujo del laboratorio de entrenamiento | Superada. |
| PE-004 | Ejecución asíncrona de la cola de trabajos | Superada. |
| PE-005 | Supervisión administrativa | Superada. |
| PE-006 | Capacidades transversales (idioma y tema) | Superada. |

Con la superación de las pruebas de sistema, la parte de verificación de vitalXAI queda completa: las pruebas automatizadas de los capítulos 34 y 35 verificaron los componentes, los flujos entre subsistemas y los mecanismos de seguridad; las pruebas de rendimiento del capítulo 36 verificaron los requisitos de rendimiento y capacidad de respuesta; y las pruebas de sistema de este capítulo verificaron los flujos completos de uso sobre el despliegue real. El conjunto de la verificación confirma que el sistema implementado satisface los requisitos funcionales y no funcionales del análisis y las condiciones definidas en el plan de pruebas.
