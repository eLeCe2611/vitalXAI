# Capítulo 33: Introducción a la verificación del sistema

La parte de verificación de la memoria presenta los resultados de las pruebas realizadas sobre el sistema vitalXAI, describiendo cómo se comprobó que la implementación satisface los requisitos funcionales y no funcionales del análisis. El plan de pruebas del capítulo 16 definió las verificaciones previstas del sistema, con sus códigos y sus criterios de éxito, y la estrategia de verificación del capítulo 25 especificó los entornos y los niveles de prueba; esta parte recoge la ejecución de esa verificación y sus resultados, de modo que la memoria documenta tanto lo que se planificó como lo que se comprobó realmente. La verificación se apoya en la batería de pruebas automatizadas del proyecto y en las comprobaciones estáticas de calidad, cuya metodología se describió en la introducción a la codificación del capítulo 27 (Myers, Sandler, & Badgett, 2011).

La parte se organiza en cuatro capítulos. Este capítulo introductorio presenta el alcance de la verificación, los entornos y las herramientas empleadas y la organización de la parte; el capítulo 34 describe las pruebas automatizadas, unitarias y de integración, con sus resultados; el capítulo 35 describe las pruebas de seguridad; y el capítulo 36 describe las pruebas de sistema y la validación funcional de los flujos completos de uso. Las pruebas de rendimiento PR-001 a PR-005 quedan identificadas como trabajo pendiente y no se presentan como resultados obtenidos.

La verificación de vitalXAI se ejecutó sobre la implementación descrita en la parte de codificación, siguiendo la estrategia definida en el capítulo 25: la batería automatizada se ejecutó en los entornos unitario y de integración, con dobles y SQLite en memoria, y las pruebas de sistema se documentaron sobre el despliegue de la plataforma. Los resultados de la ejecución y de las comprobaciones estáticas, que se detallan en los capítulos siguientes, documentan el alcance realmente comprobado. No permiten afirmar que todos los criterios del plan estén satisfechos: las pruebas de integración ejecutadas se concentran en autenticación e historial y los flujos PI-004 a PI-007 permanecen pendientes.

## 33.1 Alcance de la verificación

El alcance de la verificación de vitalXAI abarca las cinco categorías del plan de pruebas del capítulo 16: la verificación de los componentes individuales, la verificación de los flujos entre subsistemas, las pruebas de protección y control de acceso, las pruebas de rendimiento y capacidad de respuesta, y la verificación integral de los flujos completos de uso. Las dos primeras categorías se materializan en la batería automatizada de pruebas unitarias y de integración; la tercera se materializa en las pruebas de seguridad automatizadas; y las dos últimas se definen sobre el entorno de despliegue, conforme a la estrategia del capítulo 25. La tabla siguiente resume el alcance de la verificación y su correspondencia con las categorías del plan.

| Categoría del plan | Nivel | Materialización |
|---|---|---|
| Verificación de componentes individuales | Unitario | Pruebas unitarias del directorio `tests/unit/`, por subsistema. |
| Verificación de los flujos entre subsistemas | Integración | Pruebas de integración del directorio `tests/integration/`. |
| Protección y control de acceso | Seguridad | Pruebas de seguridad automatizadas (CSRF, cabeceras, limitación, tokens). |
| Rendimiento y capacidad de respuesta | Pendiente | Pruebas PR-001 a PR-005 previstas sobre el despliegue, todavía no ejecutadas. |
| Verificación integral de los flujos completos | Sistema | Pruebas de sistema de los flujos de uso (PE-001 a PE-006). |

El alcance se define de modo que la verificación progrese desde el aislamiento de los componentes hasta la comprobación integral del sistema: cada nivel cubre un grado de fidelidad mayor con respecto al entorno real, y la superación de cada nivel es condición para considerar verificada la parte del sistema que abarca, en coherencia con los criterios de aceptación definidos en el capítulo 25.

## 33.2 Entornos y herramientas de verificación

La verificación se ejecutó en los tres entornos definidos en la estrategia de verificación del capítulo 25: el entorno unitario, sin dependencia de una red o base de datos real y con dobles de prueba; el entorno de integración, con una base de datos SQLite en memoria; y el entorno de sistema, sobre el despliegue real de la plataforma. Las herramientas empleadas son las especificadas en el capítulo 25 y en la guía de pruebas del proyecto: pytest con pytest-cov para medir la cobertura, dobles construidos principalmente con `unittest.mock` y fixtures, y las comprobaciones estáticas de ruff y mypy (pytest, 2024; Ruff, 2024; Mypy, 2024).

La ejecución de la batería automatizada y de las comprobaciones estáticas sobre la implementación actual del proyecto produjo los resultados globales que se resumen en la tabla siguiente. La batería completa de pruebas unitarias y de integración se ejecutó en el entorno de verificación automatizada, la cobertura de los módulos de la aplicación se midió sobre el código implementado y las comprobaciones estáticas se aplicaron sobre el repositorio.

| Verificación | Resultado |
|---|---|
| Batería de pruebas automatizadas | 190 pruebas superadas, sin fallos. |
| Cobertura de código | 74,04 % sobre los módulos de la aplicación, por encima del umbral del 70 %. |
| Análisis estático (ruff) | Todas las comprobaciones superadas sin errores. |
| Verificación de tipos (mypy) | Sin problemas en los módulos configurados. |

Los resultados detallados de cada nivel, incluidos la distribución de las pruebas por subsistema, la cobertura por módulo, las comprobaciones de seguridad y la evidencia funcional, se presentan en los capítulos 34 a 36. Este resumen global se desglosa allí en la verificación específica de cada componente, mecanismo y flujo.

## 33.3 Organización de la parte

La parte de verificación se organiza por niveles de prueba, de modo que cada capítulo presenta el alcance y los resultados disponibles. El capítulo 34 describe las pruebas automatizadas: las pruebas unitarias de los componentes y las pruebas de integración ejecutadas, con los ficheros de pruebas, la distribución de las verificaciones y la cobertura alcanzada. El capítulo 35 describe las pruebas de seguridad automatizadas: la protección CSRF, las cabeceras de seguridad, la limitación de peticiones y la gestión de los tokens de sesión. El capítulo 36 describe las pruebas de sistema y la validación funcional de los flujos completos de uso, presentando cada flujo con su criterio de éxito y el resultado de su verificación. Las pruebas de rendimiento previstas en el plan no disponen de resultados y quedan identificadas como trabajo pendiente. Esta organización permite distinguir lo ejecutado de lo que aún debe verificarse.

## 33.4 Trazabilidad de los objetivos específicos

La verificación de los requisitos no sustituye la revisión de los objetivos del proyecto. Para hacer explícita la relación entre ambos niveles, la tabla siguiente indica dónde se documenta cada objetivo específico y qué evidencia aporta esta parte de la memoria. En los objetivos científicos, la evidencia puede consistir en la documentación de la metodología y de la capacidad implementada; no implica por sí sola que los resultados de los modelos sean clínicamente generalizables.

| Objetivo | Evidencia principal | Comprobación en la memoria |
|---|---|---|
| OE1. Revisar el estado del arte | Capítulo 1 | Revisión documentada y utilizada como fundamento del proyecto. |
| OE2. Diseñar e implementar la arquitectura de persistencia | Capítulos 12, 14, 19, 28 y 34 | Requisitos, diseño, implementación y pruebas de persistencia e historial. |
| OE3. Diseñar e implementar el control de acceso | Capítulos 12, 20, 28, 35 y 37 | Pruebas de autenticación, sesión, seguridad y aislamiento de los flujos. |
| OE4. Implementar el pipeline de entrenamiento | Capítulos 12, 23, 31 y 37 | Metodología y orquestación documentadas; flujo del laboratorio comprobado. |
| OE5. Desarrollar el módulo de explicabilidad | Capítulos 12, 30, 31 y 37 | Implementación de mapas y métricas descrita; consulta de artefactos incluida en los flujos clínico y del laboratorio. |
| OE6. Ejecutar la validación externa y el análisis estadístico | Capítulos 12, 31 y 37 | Procedimiento de validación y comparación documentado; la disponibilidad de resultados depende de la ejecución de una sesión. |
| OE7. Garantizar la reproducibilidad y la trazabilidad | Capítulos 12, 19, 23 y 31 | Configuración, semilla, resultados y artefactos contemplados en el diseño y la implementación. |
| OE8. Desarrollar la interfaz clínica de diagnóstico asistido | Capítulos 12, 22, 32 y 36 | Flujo clínico documentado mediante la prueba PE-001. |
| OE9. Desarrollar el laboratorio MLOps y el asistente conversacional | Capítulos 12, 22, 31 y 36 | Configuración, lanzamiento y consulta de una sesión documentados mediante la prueba PE-003. |
| OE10. Diseñar e implementar el procesamiento asíncrono de tareas | Capítulos 12, 29, 36 | Ejecución sin bloqueo y gestión de la cola contempladas en PR-003 y PE-004. |
| OE11. Incorporar internacionalización | Capítulos 12, 22, 32 y 36 | Cambio de idioma documentado mediante la prueba PE-006. |

Esta tabla permite localizar la evidencia de cada objetivo sin convertir la verificación de la plataforma en una afirmación sobre la validez clínica de los modelos. Los capítulos 34 a 36 presentan los resultados de las pruebas que respaldan las comprobaciones indicadas; la interpretación de las métricas de entrenamiento y validación debe hacerse junto con sus condiciones experimentales y limitaciones.
