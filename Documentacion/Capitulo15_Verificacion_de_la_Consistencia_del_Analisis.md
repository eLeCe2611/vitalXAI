# Capítulo 15: Verificación de la consistencia del análisis

Este capítulo contrasta los elementos documentales del análisis de vitalXAI y registra las correspondencias confirmadas y las lagunas que siguen abiertas. La revisión se limita a comprobar la trazabilidad entre objetivos, requisitos, casos de uso, subsistemas y entidades del dominio. No demuestra que todas las capacidades estén implementadas ni que todos los requisitos hayan sido verificados mediante pruebas.

## 15.1 Criterio de verificación

La revisión utiliza como fuentes los objetivos del sistema del capítulo 11, la especificación de requisitos y los casos de uso del capítulo 12, la organización de subsistemas del capítulo 13 y el modelo de dominio del capítulo 14. La comprobación se plantea como una revisión de trazabilidad entre artefactos, no como una prueba de aceptación del producto (Jacobson, Booch, & Rumbaugh, 1999; Larman, 2004). Para cada relación se distingue entre tres situaciones: correspondencia documentada, correspondencia que requiere una interpretación transversal y laguna abierta. Esta distinción evita convertir una referencia existente en una certificación de cumplimiento.

## 15.2 Objetivos y requisitos

La matriz de la sección 12.1.1.7 permite comprobar una cobertura formal entre los once objetivos del sistema y los requisitos funcionales. Todos los objetivos tienen al menos un requisito asociado en esa matriz. Esta comprobación confirma que existe una relación documental, pero no permite concluir que cada objetivo esté especificado en todos sus aspectos.

El objetivo del laboratorio de entrenamiento mantiene una laguna conocida. El capítulo 11 declara que el progreso del entrenamiento por épocas está implementado y lo asocia a la prueba PU-023, pero esta capacidad no dispone de un requisito funcional propio. Por tanto, la matriz puede mostrar que OBJ-004 está relacionado con RF-017 a RF-021, RF-030 a RF-032 y RF-041, pero no demuestra que el progreso por épocas esté cubierto por la especificación. Esta cuestión queda abierta para una revisión posterior del catálogo.

La situación del informe individual del diagnóstico se ha actualizado en el capítulo 11: el capítulo 12 ya contiene RF-039 y lo asocia a PU-017. Por ello, esa laguna queda cerrada a nivel de trazabilidad documental; la ejecución y el resultado de la prueba deben comprobarse en los capítulos de verificación correspondientes.

| Resultado de la revisión | Estado |
|---|---|
| Cada objetivo tiene al menos un requisito asociado en la matriz del capítulo 12. | Confirmado como relación documental. |
| El progreso del entrenamiento por épocas tiene un requisito funcional propio. | No confirmado. La laguna permanece abierta. |
| El informe individual del diagnóstico tiene un requisito funcional propio. | Confirmado mediante RF-039; su prueba está asociada a PU-017. |
| La existencia de una relación objetivo requisito demuestra que el objetivo está completamente especificado. | No confirmado. |

## 15.3 Requisitos, casos de uso y subsistemas

La matriz de la sección 12.2.4 establece relaciones entre los requisitos funcionales y los casos de uso. La revisión confirma que los requisitos funcionales enumerados en esa matriz tienen una referencia a uno o más casos de uso, con la excepción de RF-005 y RF-006, que son requisitos transversales y condicionan otras interacciones en lugar de constituir casos de uso independientes.

Esta correspondencia tampoco prueba que las funcionalidades estén implementadas. Solo demuestra que la especificación funcional tiene una relación explícita con su comportamiento esperado. En particular, la asociación del progreso del entrenamiento con PU-023 no elimina la ausencia de un requisito funcional específico para esa capacidad.

El capítulo 13 conserva los identificadores SS-001 a SS-006 y documenta su correspondencia con los seis módulos del capítulo 12. Esta relación es útil para ordenar las secuencias del capítulo 14 y las pruebas posteriores, pero no constituye una descomposición independiente ni permite concluir que se hayan demostrado formalmente los niveles de cohesión y acoplamiento.

| Comprobación | Resultado |
|---|---|
| Los requisitos funcionales aparecen relacionados con casos de uso en la matriz del capítulo 12. | Confirmado a nivel documental. |
| RF-005 y RF-006 tienen casos de uso independientes. | No aplica; son requisitos transversales. |
| Cada caso de uso se organiza mediante un identificador de subsistema. | Confirmado mediante la correspondencia del capítulo 13. |
| La organización de subsistemas demuestra por sí sola una arquitectura de bajo acoplamiento. | No confirmado. Esa decisión corresponde al diseño posterior. |

## 15.4 Requisitos no funcionales y responsabilidades

La asignación de requisitos no funcionales a subsistemas debe interpretarse como una indicación de ámbito principal, porque muchos de estos requisitos afectan a más de un subsistema. La tabla siguiente identifica el ámbito principal de cada grupo y evita presentar esa asignación como una responsabilidad exclusiva o como una certificación de cumplimiento.

| Grupo de requisitos | Requisitos | Ámbito principal de aplicación |
|---|---|---|
| Seguridad del acceso | RNF-001 a RNF-005, RNF-007, RNF-008, RNF-010 y RNF-011 | SS-001, con aplicación transversal al resto de la plataforma. |
| Auditoría y eventos de seguridad | RNF-006 y RNF-009 | SS-005, con apoyo de los componentes que ejecutan las operaciones supervisadas. |
| Confidencialidad y protección de datos | RNF-012 a RNF-018 | Transversal a SS-001, SS-002, SS-003, SS-004 y SS-005. |
| Rendimiento y capacidad de respuesta | RNF-019 a RNF-022 | SS-002, SS-004 y SS-006 según la operación afectada. |
| Usabilidad, internacionalización y accesibilidad | RNF-023 a RNF-026 | SS-006 y las interfaces de los demás subsistemas. |
| Robustez y disponibilidad | RNF-027 a RNF-030 | SS-006 como ámbito de la cola, con efecto sobre SS-002 y SS-004. |
| Persistencia y salvaguarda de los datos | RNF-031 y RNF-032 | SS-003, SS-004 y los servicios compartidos de persistencia. |
| Reproducibilidad | RNF-033 y RNF-034 | SS-004. |
| Proceso y entregables | RNF-035 a RNF-038 | Transversal al proyecto, no asignable a un único subsistema. |

La tabla asigna a cada grupo un ámbito principal coherente con la organización de los capítulos 12 y 13, pero no confirma que todos estén implementados. En el capítulo 12 constan como aprobados y pendientes los requisitos RNF-006, RNF-009, RNF-016, RNF-017, RNF-021, RNF-022, RNF-029 y RNF-032. Por tanto, no puede afirmarse que todos los requisitos no funcionales estén satisfechos o verificados en el estado actual.

## 15.5 Modelo de dominio y limitaciones

El capítulo 14 contiene once entidades conceptuales. La incorporación de ResultadoPliegue permite representar las métricas de cada pliegue de validación cruzada. ResultadoValidacionExterna representa los resultados de cada modelo sobre la cohorte independiente y ComparacionModelos representa los contrastes entre pares de modelos, incluido el p-valor del test de DeLong (DeLong, DeLong, & Clarke-Pearson, 1988). Estas relaciones hacen que el modelo de dominio sea compatible con RF-022 y RF-029 a nivel conceptual.

La verificación del modelo de dominio tiene un alcance limitado. El capítulo 19 materializa parte de estas entidades mediante ficheros y no mediante tablas. En particular, las carpetas de sesiones y resultados del laboratorio no incluyen una asociación física con `user_id`, por lo que RF-005 y OBJ-008 no quedan respaldados de forma equivalente a las entidades almacenadas en tablas. La existencia de una clase conceptual no demuestra que todos sus datos estén disponibles ni aislados correctamente en la implementación actual. Esta limitación debe resolverse en una evolución posterior y comprobarse mediante pruebas específicas del laboratorio.

## 15.6 Resultado de la verificación

La revisión confirma las siguientes correspondencias: los objetivos tienen referencias a requisitos, los requisitos funcionales tienen referencias a casos de uso, los casos de uso conservan identificadores de subsistema y el modelo de dominio contempla las métricas por pliegue y las comparaciones entre modelos.

También confirma las siguientes limitaciones:

- El progreso del entrenamiento por épocas se declara implementado y asociado a PU-023, pero no tiene un requisito funcional propio ni un resultado de verificación documentado en este capítulo.
- Los requisitos no funcionales pendientes no pueden considerarse satisfechos ni verificados.
- La asignación de requisitos no funcionales a subsistemas indica ámbitos principales, pero no demuestra una responsabilidad exclusiva ni un cumplimiento efectivo.
- La existencia de matrices de trazabilidad no demuestra por sí sola la implementación ni la validación del sistema.

La situación de los requisitos que el capítulo 12 identifica como pendientes se resume a continuación. La tabla distingue la falta de implementación de la falta de evidencia de verificación, porque no representan la misma situación.

| Requisito | Situación | Evidencia o limitación |
|---|---|---|
| RF-019 | Pendiente de implementación | La selección de rutas aún no está confinada al directorio permitido. |
| RF-037 | Implementación parcial | Se cancelan trabajos pendientes, pero no se interrumpen trabajos en ejecución. |
| RF-040 | Pendiente de implementación | La gestión administrativa de cuentas no está disponible en el prototipo. |
| RF-041 | Pendiente de implementación | No se aplican límites de entrenamientos simultáneos o encolados. |
| RNF-006, RNF-009 | Pendientes de implementación | No existe auditoría administrativa ni registro formal de eventos de seguridad. |
| RNF-016, RNF-017 | Pendientes de implementación | La política completa de retención y el cifrado de datos en reposo no están implementados. |
| RNF-021, RNF-022 | Pendientes de verificación | Falta evidencia de las pruebas de concurrencia y del comportamiento con la GPU ocupada. |
| RNF-029, RNF-032 | Pendientes de implementación | No están implementadas la recuperación completa tras reinicio ni la copia de seguridad y restauración. |

En consecuencia, el análisis es trazable en sus relaciones principales, pero no puede certificarse como completamente consistente ni cerrado sin resolver la laguna del progreso del entrenamiento y sin aportar la verificación de los requisitos pendientes. Estas conclusiones se mantienen explícitas para que los capítulos de diseño, implementación y pruebas no presenten como demostrado aquello que el análisis todavía identifica como abierto.
