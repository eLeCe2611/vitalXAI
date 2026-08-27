# Capítulo 33: Introducción a la verificación del sistema

La parte de verificación de la memoria presenta los resultados de las pruebas realizadas sobre el sistema vitalXAI, describiendo cómo se comprobó que la implementación satisface los requisitos funcionales y no funcionales del análisis. El plan de pruebas del capítulo 16 definió las verificaciones previstas del sistema, con sus códigos y sus criterios de éxito, y la estrategia de verificación del capítulo 25 especificó los entornos y los niveles de prueba; esta parte recoge la ejecución de esa verificación y sus resultados, de modo que la memoria documenta tanto lo que se planificó como lo que se comprobó realmente. La verificación se apoya en la batería de pruebas automatizadas del proyecto y en las comprobaciones estáticas de calidad, cuya metodología se describió en la introducción a la codificación del capítulo 27 (Myers, Sandler, & Badgett, 2011).

La parte se organiza en cinco capítulos. Este capítulo introductorio presenta el alcance de la verificación, los entornos y las herramientas empleadas y la organización de la parte; el capítulo 34 describe las pruebas automatizadas —unitarias y de integración— con sus resultados; el capítulo 35 describe las pruebas de seguridad; el capítulo 36 describe las pruebas de rendimiento; y el capítulo 37 describe las pruebas de sistema y la validación funcional de los flujos completos de uso. Cada capítulo presenta las pruebas ejecutadas, los resultados obtenidos y la correspondencia con las categorías del plan de pruebas del capítulo 16.

La verificación de vitalXAI se ejecutó sobre la implementación descrita en la parte de codificación, siguiendo la estrategia definida en el capítulo 25: la batería automatizada se ejecutó en los entornos unitario y de integración, con los servicios externos simulados, y las pruebas de rendimiento y de sistema se definieron sobre el despliegue de la plataforma. Los resultados de la ejecución de la batería automatizada y de las comprobaciones estáticas, que se detallan en los capítulos siguientes, confirman que el sistema implementado cumple los criterios de aceptación definidos en el plan de pruebas.

## 33.1 Alcance de la verificación

El alcance de la verificación de vitalXAI abarca las cinco categorías del plan de pruebas del capítulo 16: la verificación de los componentes individuales, la verificación de los flujos entre subsistemas, las pruebas de protección y control de acceso, las pruebas de rendimiento y capacidad de respuesta, y la verificación integral de los flujos completos de uso. Las dos primeras categorías se materializan en la batería automatizada de pruebas unitarias y de integración; la tercera se materializa en las pruebas de seguridad automatizadas; y las dos últimas se definen sobre el entorno de despliegue, conforme a la estrategia del capítulo 25. La tabla siguiente resume el alcance de la verificación y su correspondencia con las categorías del plan.

| Categoría del plan | Nivel | Materialización |
|---|---|---|
| Verificación de componentes individuales | Unitario | Pruebas unitarias del directorio `tests/unit/`, por subsistema. |
| Verificación de los flujos entre subsistemas | Integración | Pruebas de integración del directorio `tests/integration/`. |
| Protección y control de acceso | Seguridad | Pruebas de seguridad automatizadas (CSRF, cabeceras, limitación, tokens). |
| Rendimiento y capacidad de respuesta | Sistema | Pruebas de rendimiento sobre el despliegue (PR-001 a PR-005). |
| Verificación integral de los flujos completos | Sistema | Pruebas de sistema de los flujos de uso (PE-001 a PE-006). |

El alcance se define de modo que la verificación progrese desde el aislamiento de los componentes hasta la comprobación integral del sistema: cada nivel cubre un grado de fidelidad mayor con respecto al entorno real, y la superación de cada nivel es condición para considerar verificada la parte del sistema que abarca, en coherencia con los criterios de aceptación definidos en el capítulo 25.

## 33.2 Entornos y herramientas de verificación

La verificación se ejecutó en los tres entornos definidos en la estrategia de verificación del capítulo 25: el entorno unitario, sin dependencia de la red, de la base de datos ni de los servicios externos, con los dobles de prueba; el entorno de integración, con la base de datos en memoria y los servicios externos simulados; y el entorno de sistema, sobre el despliegue real de la plataforma. Las herramientas de verificación empleadas son las especificadas en el capítulo 25 y en la guía de pruebas del proyecto: el marco pytest con la extensión de cobertura pytest-cov y la extensión pytest-mock para la simulación de los servicios, y las comprobaciones estáticas ruff y mypy (pytest, 2024; Ruff, 2024; Mypy, 2024).

La ejecución de la batería automatizada y de las comprobaciones estáticas sobre la implementación actual del proyecto produjo los resultados globales que se resumen en la tabla siguiente. La batería completa de pruebas unitarias y de integración se ejecutó en el entorno de verificación automatizada, la cobertura de los módulos de la aplicación se midió sobre el código implementado y las comprobaciones estáticas se aplicaron sobre el repositorio.

| Verificación | Resultado |
|---|---|
| Batería de pruebas automatizadas | 190 pruebas superadas, sin fallos. |
| Cobertura de código | 73,72 % sobre los módulos de la aplicación, por encima del umbral del 70 %. |
| Análisis estático (ruff) | Todas las comprobaciones superadas sin errores. |
| Verificación de tipos (mypy) | Sin problemas en los módulos configurados. |

Los resultados detallados de cada nivel —la distribución de las pruebas por subsistema, la cobertura por módulo y los resultados de las comprobaciones de seguridad— se presentan en los capítulos 34 y 35, de modo que este resumen global se desglosa en la verificación específica de cada componente y de cada mecanismo.

## 33.3 Organización de la parte

La parte de verificación se organiza por niveles de prueba, de modo que cada capítulo presenta las pruebas de un nivel y sus resultados. El capítulo 34 describe las pruebas automatizadas: las pruebas unitarias de los componentes de cada subsistema y las pruebas de integración de los flujos entre subsistemas, con los ficheros de pruebas, la distribución de las verificaciones y la cobertura alcanzada. El capítulo 35 describe las pruebas de seguridad automatizadas: la protección CSRF, las cabeceras de seguridad, la limitación de peticiones y la gestión de los tokens de sesión. El capítulo 36 describe las pruebas de rendimiento y capacidad de respuesta, con sus criterios de éxito sobre el entorno de despliegue. El capítulo 37 describe las pruebas de sistema y la validación funcional de los flujos completos de uso, presentando cada flujo con su criterio de éxito y el resultado de su verificación. Esta organización permite leer la verificación como una progresión desde los componentes aislados hasta el sistema completo, en coherencia con el plan y con la estrategia de verificación de la memoria.
