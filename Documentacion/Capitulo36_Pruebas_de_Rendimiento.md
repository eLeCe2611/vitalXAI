# Capítulo 36: Pruebas de rendimiento

Las pruebas de rendimiento verifican que la plataforma satisface los requisitos no funcionales de rendimiento y capacidad de respuesta definidos en el análisis: el tiempo de respuesta de la inferencia (RNF-019), la ejecución sin bloqueo de la interfaz durante las tareas de larga duración (RNF-020) y la capacidad de acceso concurrente (RNF-021) (Myers, Sandler, & Badgett, 2011). Este capítulo describe las pruebas de rendimiento del plan de pruebas del capítulo 16 —los códigos PR-001 a PR-005—, sus criterios de éxito y las condiciones de medición sobre el entorno de despliegue. A diferencia de las pruebas automatizadas de los capítulos 34 y 35, estas verificaciones se ejecutan sobre el sistema real, de modo que los resultados reflejan la infraestructura de operación y no los dobles de prueba.

Las pruebas de rendimiento se corresponden con la categoría de rendimiento y capacidad de respuesta del plan de pruebas del capítulo 16, y su ejecución se define sobre el entorno de sistema de la estrategia de verificación del capítulo 25, con el despliegue completo de la plataforma: el servidor de aplicación, la base de datos MySQL, los pesos de los modelos y el worker de la cola. Los criterios de éxito se fijan en función del comportamiento esperado del sistema, y los umbrales concretos de tiempo se ajustan tras una primera campaña de medición sobre el entorno de despliegue, de modo que los criterios reflejen la infraestructura real de la plataforma.

## 36.1 Rendimiento de la inferencia

Las pruebas PR-001 y PR-002 verifican el rendimiento del diagnóstico asistido, asociadas al requisito RNF-019, que exige que el sistema gestione la carga de los modelos de forma eficiente. La prueba PR-001 verifica que la primera inferencia sobre una radiografía se completa en un tiempo razonable, asumiendo el coste de la carga de los pesos del modelo; la prueba PR-002 verifica que las inferencias posteriores sobre el mismo modelo son casi instantáneas, al reutilizar los pesos ya cargados en memoria. La tabla siguiente resume estas verificaciones y sus criterios.

| ID | Verificación | Criterio de éxito |
|---|---|---|
| PR-001 | La primera inferencia sobre una radiografía se completa en un tiempo razonable. | La primera consulta con cada arquitectura carga el modelo y produce el resultado en un tiempo que no hace incómodo el uso de la herramienta. |
| PR-002 | Las inferencias posteriores son casi instantáneas. | Las consultas siguientes sobre el mismo modelo se completan de forma sensiblemente más rápida que la primera, al reutilizar los pesos ya cargados. |

La verificación de estas pruebas se apoya en el mecanismo de caché de modelos implementado en el motor de inferencia, descrito en la codificación del capítulo 30: la primera consulta con cada arquitectura paga la carga de los pesos, mientras que las posteriores reutilizan el modelo en memoria. La medición se realiza sobre el entorno de despliegue con radiografías de prueba, registrando el tiempo de cada consulta para comparar la primera con las siguientes.

## 36.2 Ejecución sin bloqueo de la interfaz

La prueba PR-003 verifica la ejecución sin bloqueo de la interfaz durante las tareas de larga duración, asociada al requisito RNF-020, que exige que los procesos intensivos se ejecuten de forma asíncrona sin bloquear la interfaz. La prueba comprueba que, durante un entrenamiento o un análisis de explicabilidad del laboratorio, la plataforma continúa respondiendo a las peticiones del usuario. La tabla siguiente resume esta verificación.

| ID | Verificación | Criterio de éxito |
|---|---|---|
| PR-003 | La interfaz permanece operativa durante una tarea de larga duración. | Durante un entrenamiento o un análisis de explicabilidad, la plataforma continúa respondiendo a las peticiones del usuario sin bloquearse. |

La verificación de esta prueba se apoya en la ejecución asíncrona implementada en el capítulo 29: el worker procesa los trabajos fuera del ciclo de petición mediante el executor de eventos, de modo que la interfaz permanece operativa mientras la cola procesa los entrenamientos. La prueba se realiza lanzando una tarea de larga duración en el laboratorio y comprobando, durante su ejecución, que la aplicación responde a otras peticiones, como la consulta del estado de la cola o la navegación entre las ventanas.

## 36.3 Acceso concurrente

Las pruebas PR-004 y PR-005 verifican la capacidad de la plataforma para soportar el acceso concurrente, asociadas al requisito RNF-021, que exige la gestión del acceso concurrente mediante el pool de conexiones. La prueba PR-004 comprueba que el sistema soporta una carga razonable de usuarios concurrentes sin una degradación significativa del tiempo de respuesta; la prueba PR-005 comprueba que el pool de conexiones gestiona el acceso concurrente a la base de datos sin errores de conexión ni contención excesiva. La tabla siguiente resume estas verificaciones.

| ID | Verificación | Criterio de éxito |
|---|---|---|
| PR-004 | El sistema soporta la carga de varios usuarios concurrentes. | Con un número razonable de usuarios concurrentes, el tiempo de respuesta no se degrada de forma significativa. |
| PR-005 | El pool de conexiones gestiona el acceso concurrente a la base de datos. | Las peticiones concurrentes se atienden sin errores de conexión ni contención excesiva. |

La verificación de estas pruebas se apoya en la gestión del pool de conexiones implementado en la capa de persistencia, descrito en la codificación del capítulo 28: el pool configura un número de conexiones que las peticiones concurrentes reutilizan, de modo que no se abre una conexión por operación. La prueba se realiza con un conjunto de usuarios concurrentes que ejecutan operaciones habituales de la plataforma, observando el tiempo de respuesta y la ausencia de errores de conexión.

## 36.4 Condiciones de medición

Las pruebas de rendimiento se ejecutan sobre el entorno de despliegue descrito en el capítulo 26, con la configuración de infraestructura del sistema en operación. Las condiciones de medición incluyen la infraestructura del servidor —el proceso de aplicación, la base de datos MySQL y los artefactos del aprendizaje automático— y la carga de trabajo de la prueba, que emplea radiografías de prueba y operaciones representativas de los flujos de la plataforma. Los umbrales concretos de tiempo para las pruebas PR-001 a PR-004 se fijan tras una primera campaña de medición sobre el entorno de despliegue, de modo que los criterios reflejen la infraestructura real y no valores especulativos; la estrategia de verificación del capítulo 25 establece que estos umbrales se ajustan con los datos medidos.

Las pruebas de rendimiento completan la verificación de los requisitos no funcionales de rendimiento y capacidad de respuesta de la plataforma, junto con las verificaciones automatizadas de los capítulos 34 y 35. Con las pruebas de rendimiento descritas, la parte de verificación aborda en el capítulo siguiente las pruebas de sistema y la validación funcional de los flujos completos de uso, que verifican el comportamiento integral de la plataforma sobre el despliegue real.
