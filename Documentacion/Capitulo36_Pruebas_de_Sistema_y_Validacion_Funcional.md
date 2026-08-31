# Capítulo 36: Pruebas de sistema y validación funcional

Este capítulo reúne la evidencia funcional obtenida al recorrer vitalXAI desde su interfaz. Se describen las seis pruebas de sistema del plan de pruebas del capítulo 16, identificadas como PE-001 a PE-006, junto con sus pasos, criterios de éxito y alcance. Las comprobaciones se realizaron manualmente sobre el despliegue definido en el capítulo 25 y cada flujo se acompaña de una captura de la aplicación en funcionamiento. Este enfoque sigue la comprobación de flujos completos entre componentes propia de las pruebas de sistema (Myers, Sandler, & Badgett, 2011).

Las pruebas de sistema verifican los seis flujos completos de la plataforma: el flujo clínico del diagnóstico, la gestión del historial, el flujo del laboratorio de entrenamiento, la ejecución asíncrona de la cola, la supervisión administrativa y las capacidades transversales de idioma y tema. Cada prueba recorre las operaciones del flujo sobre la interfaz real, desde el registro o el acceso hasta la obtención del resultado, y comprueba que el comportamiento coincide con el especificado en los casos de uso del análisis. La ejecución de cada prueba se apoya en la documentación de operación de la plataforma y en las cuentas de acceso del entorno de despliegue.

## 36.1 PE-001: Flujo clínico completo

La prueba PE-001 verifica el flujo clínico completo del diagnóstico asistido: la subida de una radiografía, la selección del modelo, la solicitud del diagnóstico, la visualización del resultado y de los mapas de explicabilidad, y la generación del informe PDF. La prueba se inicia desde el panel de diagnóstico del usuario autenticado y recorre las operaciones descritas en los casos de uso CU-005 a CU-010 y CU-037. Los pasos de la prueba son los siguientes.

1. El usuario autenticado accede al panel de diagnóstico.
2. El usuario sube una radiografía de tórax en la zona de carga.
3. El usuario selecciona una arquitectura de inteligencia artificial.
4. El usuario solicita el diagnóstico y espera el procesamiento en la cola.
5. El sistema muestra el resultado con la etiqueta, la confianza y el modelo empleado.
6. El usuario visualiza los mapas de explicabilidad y el sistema genera el informe PDF de la consulta.

El criterio de éxito de la prueba es que el flujo completo se realiza sin errores y el profesional obtiene el diagnóstico, su confianza y los mapas de explicabilidad, mientras el sistema genera el informe de la consulta. El resultado esperado se confirma con la captura del panel de diagnóstico mostrando el resultado y los artefactos generados.

*Ilustración 1 - Flujo de diagnóstico completado con resultado, mapas de explicabilidad e informe*

## 36.2 PE-002: Gestión del historial

La prueba PE-002 verifica la gestión del historial de consultas: la consulta del listado, el detalle de una consulta, el renombrado y la eliminación. La prueba se realiza desde el panel de diagnóstico, sobre las consultas del usuario, y recorre las operaciones descritas en los casos de uso CU-011 a CU-014. Los pasos de la prueba son los siguientes.

1. El usuario consulta su historial de consultas en el panel.
2. El usuario abre el detalle de una consulta del listado.
3. El usuario renombra la consulta con un nuevo nombre visible.
4. El usuario elimina una consulta, confirmando la operación.

El criterio de éxito de la prueba es que todas las operaciones del historial se ejecutan correctamente, el listado se actualiza después de los cambios y el aislamiento de datos entre usuarios se respeta. El resultado esperado se confirma con la captura del historial y del detalle de una consulta.

*Ilustración 2 - Historial de consultas con su detalle*

## 36.3 PE-003: Flujo del laboratorio

La prueba PE-003 verifica el flujo del laboratorio de entrenamiento: la conversación con el asistente, el lanzamiento del experimento, la consulta de las sesiones y de los resultados, y la generación del informe PDF de la sesión. La prueba se realiza desde el laboratorio del usuario investigador y recorre las operaciones descritas en los casos de uso CU-015 a CU-030. Los pasos de la prueba son los siguientes.

1. El usuario accede al laboratorio de entrenamiento.
2. El usuario configura el experimento con el asistente conversacional y selecciona la carpeta del dataset.
3. El usuario lanza el experimento y lo encola en segundo plano.
4. El usuario consulta la sesión, el ranking de modelos y los resultados de un modelo.
5. El usuario genera el informe PDF de la sesión.

El criterio de éxito de la prueba es que el experimento se configura y lanza mediante el asistente, se ejecuta en segundo plano y sus resultados e informe se obtienen sin errores. El resultado esperado se confirma con la captura de la vista de resultados de la sesión.

*Ilustración 3 - Laboratorio de entrenamiento con la vista de resultados de la sesión*

## 36.4 PE-004: Ejecución asíncrona de la cola

La prueba PE-004 verifica la ejecución asíncrona de la cola de trabajos: la consulta del estado de la cola y la cancelación de un trabajo pendiente. La prueba se realiza desde el panel de diagnóstico o el laboratorio, y recorre las operaciones descritas en los casos de uso CU-034 y CU-035. Los pasos de la prueba son los siguientes.

1. El usuario consulta el panel de la cola de trabajos.
2. El usuario comprueba el estado de sus trabajos encolados o en ejecución; la finalización o el fallo se muestran en el mensaje del diagnóstico o en la consola del laboratorio.
3. El usuario cancela un trabajo pendiente, confirmando la operación.

El criterio de éxito de la prueba es que el usuario conoce el estado de sus trabajos y puede cancelar un trabajo pendiente, mientras que un trabajo en ejecución no se interrumpe. El resultado esperado se confirma con la captura del panel de la cola de trabajos.

*Ilustración 4 - Panel de la cola de trabajos con su estado*

## 36.5 PE-005: Supervisión administrativa

La prueba PE-005 verifica la supervisión administrativa de la plataforma: el listado de usuarios, la consulta de las consultas de un usuario y su detalle. La prueba se realiza desde el panel del usuario con rol de administrador, y recorre las operaciones descritas en los casos de uso CU-031 a CU-033. Los pasos de la prueba son los siguientes.

1. El administrador abre el panel de administración desde su ventana.
2. El administrador consulta el listado de usuarios con sus recuentos de actividad.
3. El administrador consulta las consultas de un usuario concreto y el detalle de una consulta.

El criterio de éxito de la prueba es que el administrador supervisa la actividad de un usuario concreto desde el panel de administración, con la comprobación de rol aplicada por el sistema. El resultado esperado se confirma con la captura del diálogo de administración.

*Ilustración 5 - Supervisión administrativa de la actividad de un usuario*

## 36.6 PE-006: Capacidades transversales

La prueba PE-006 verifica las capacidades transversales de la plataforma: el cambio de idioma y el cambio del tema visual de la interfaz. La prueba se realiza desde cualquiera de las ventanas del sistema y recorre las operaciones descritas en los casos de uso CU-004 y CU-036. Los pasos de la prueba son los siguientes.

1. El usuario cambia el idioma de la interfaz mediante el selector de idioma.
2. El sistema aplica las traducciones en toda la interfaz sin recargar la página.
3. El usuario alterna el tema visual entre el claro y el oscuro.
4. El sistema aplica el tema en toda la interfaz y conserva la preferencia.

El criterio de éxito de la prueba es que el idioma y el tema se aplican en toda la interfaz sin interrumpir la navegación. El resultado esperado se confirma con la captura de una ventana en el idioma y el tema seleccionados.

*Ilustración 6 - Interfaz de la plataforma con el idioma y el tema seleccionados*

## 36.7 Resultados de la validación funcional

Las seis pruebas de sistema documentan los flujos principales de uso de la plataforma sobre el despliegue real, cubriendo el diagnóstico, el historial, el laboratorio, la cola, la administración y las capacidades transversales. La gestión funcional del historial se comprueba, pero el aislamiento entre dos usuarios no cuenta con una verificación de extremo a extremo documentada. La tabla siguiente resume el resultado de la validación funcional.

| ID | Flujo verificado | Resultado |
|---|---|---|
| PE-001 | Flujo clínico completo del diagnóstico | Comprobación funcional documentada. |
| PE-002 | Gestión del historial de consultas | Comprobación funcional documentada. El aislamiento entre dos usuarios no queda verificado de extremo a extremo. |
| PE-003 | Flujo del laboratorio de entrenamiento | Comprobación funcional documentada. |
| PE-004 | Ejecución asíncrona de la cola de trabajos | Comprobación funcional documentada. |
| PE-005 | Supervisión administrativa | Comprobación funcional documentada. |
| PE-006 | Capacidades transversales (idioma y tema) | Comprobación funcional documentada. |

Las capturas incluidas en este capítulo son evidencia ilustrativa de una ejecución manual, pero no constituyen por sí solas una validación reproducible: no se documentan de forma completa los datos de entrada, la identidad de la persona que ejecutó cada flujo, la fecha, el entorno exacto ni un registro detallado de cada resultado. Por ello, el estado de las seis pruebas se expresa como comprobación funcional documentada y no como superación completa.

La verificación documentada no permite afirmar que todos los requisitos estén satisfechos. Las pruebas automatizadas de los capítulos 34 y 35 respaldan los componentes ejecutados y los mecanismos de seguridad cubiertos, pero las cuatro pruebas de integración se concentran en autenticación. Las pruebas PI-004 a PI-007, incluido el aislamiento de datos entre usuarios exigido por RF-005, permanecen pendientes. Tampoco existe verificación documentada de los requisitos de protección de datos, anonimización, retención, copias de seguridad y recuperación tras reinicio. Las pruebas de rendimiento PR-001 a PR-005 no se han ejecutado, por lo que no existe evidencia para declarar verificados RNF-019, RNF-020 y RNF-021. Finalmente, no se realizó una evaluación con usuarios reales que respalde empíricamente los requisitos de usabilidad y accesibilidad. El conjunto de resultados debe interpretarse, por tanto, como evidencia parcial del comportamiento de la plataforma y no como una certificación completa del cumplimiento del catálogo.
