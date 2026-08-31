# Capítulo 13: Identificación de subsistemas de análisis

El capítulo 12 organiza los requisitos funcionales y los casos de uso en seis módulos: autenticación y cuenta, diagnóstico clínico, historial de consultas, laboratorio MLOps, administración y capacidades transversales. Este capítulo conserva esa organización mediante la nomenclatura de subsistemas utilizada en los capítulos posteriores. No introduce una descomposición distinta ni toma decisiones de diseño; establece la correspondencia entre los módulos funcionales y los identificadores que se utilizarán en el análisis dinámico y en las pruebas.

La correspondencia es la siguiente:

| Módulo funcional del capítulo 12 | Subsistema de análisis | Contenido principal |
|---|---|---|
| Módulo de autenticación y cuenta | SS-001, Subsistema de acceso y gestión de cuentas | Registro, inicio y cierre de sesión, cambio de idioma, aislamiento de datos y control de roles. |
| Módulo de diagnóstico clínico | SS-002, Subsistema de diagnóstico asistido | Acceso al panel, carga de radiografías, diagnóstico, resultados, explicabilidad e informes de las consultas. |
| Módulo de historial de consultas | SS-003, Subsistema de gestión del historial de consultas | Consulta, detalle, renombrado y eliminación de consultas propias. |
| Módulo de laboratorio MLOps | SS-004, Subsistema de laboratorio de experimentación MLOps | Configuración, entrenamiento, resultados, explicabilidad, comparación, validación externa, informes de experimentación y limitación prevista de entrenamientos. |
| Módulo de administración | SS-005, Subsistema de supervisión y administración | Consulta de usuarios, supervisión de consultas y gestión prevista de cuentas por parte del administrador. |
| Módulo transversal | SS-006, Subsistema de capacidades transversales | Consulta y cancelación de trabajos de la cola y personalización del tema visual. |

La cola de trabajos es un mecanismo común del sistema del que dependen el diagnóstico, el laboratorio y la validación externa. Por ese motivo, su relación con SS-002 y SS-004 se tratará como una dependencia entre subsistemas, no como una capacidad exclusiva de un único ámbito funcional. El cambio de tema visual se mantiene en SS-006 porque pertenece al módulo transversal definido en el capítulo 12 y no forma parte de un flujo clínico, de laboratorio o de administración.

Esta organización permite conservar la trazabilidad sin duplicar la especificación de requisitos ni los casos de uso. El capítulo 14 utiliza estos identificadores para ordenar las secuencias de interacción y el capítulo 15 comprueba la correspondencia entre requisitos, casos de uso y subsistemas. Las decisiones sobre componentes, tecnologías y distribución de responsabilidades internas se reservan para los capítulos de diseño.

Por tanto, los subsistemas de este capítulo deben entenderse como identificadores estables para organizar el análisis. La descripción detallada de cada capacidad, sus condiciones y sus flujos se encuentra en el capítulo 12, que es la referencia principal para los requisitos y los casos de uso.
