# Capítulo 38: Valoración final del proyecto vitalXAI

Este capítulo valora el proyecto vitalXAI como solución tecnológica. A diferencia del capítulo 37, centrado en el aprendizaje y en el proceso académico del TFG, aquí se analizan las aportaciones del sistema, las capacidades desarrolladas, la evidencia obtenida y las limitaciones que condicionan su uso.

## 38.1 Valoración global del proyecto

vitalXAI ha materializado una plataforma web MLOps orientada a la experimentación con inteligencia artificial explicable aplicada al diagnóstico asistido de neumonía mediante radiografías de tórax. El proyecto integra en un mismo entorno el diagnóstico, la generación de explicaciones, el entrenamiento de modelos, la comparación de resultados, la validación externa y la gestión de los artefactos producidos.

La principal aportación del proyecto es la integración de estas capacidades en un flujo accesible desde una interfaz web. El usuario puede realizar una consulta de diagnóstico, visualizar el resultado y sus mapas de explicabilidad y descargar un informe. Del mismo modo, el investigador puede configurar un experimento mediante el asistente conversacional, lanzarlo en segundo plano, consultar su progreso y revisar sus resultados. La cola de trabajos permite separar las operaciones de larga duración de las peticiones web y evita que el entrenamiento bloquee la interfaz.

## 38.2 Aportaciones técnicas

El sistema aporta una arquitectura que separa la interfaz, los routers, los servicios, la persistencia y los procesos de cálculo. Esta organización facilita la evolución independiente del diagnóstico, el laboratorio MLOps y los mecanismos transversales de autenticación, internacionalización y generación de informes.

En el ámbito del aprendizaje automático, el proyecto prepara un pipeline para diecinueve arquitecturas, dieciséis CNN y tres Transformers, con validación cruzada estratificada, almacenamiento de configuraciones y resultados y análisis de explicabilidad y calibración. Las técnicas XAI permiten generar mapas visuales y calcular métricas como Deletion AUC, Insertion AUC, Sparsity, Entropy y Stability SSIM. La plataforma también incorpora comparación estadística y validación externa mediante una cohorte independiente.

En el ámbito de la ingeniería del software, se han incorporado autenticación, autorización, protección CSRF, gestión de tokens, limitación de peticiones, cabeceras de seguridad, persistencia de historiales, generación de informes PDF e internacionalización. La batería descrita en los capítulos 34 y 35 incluye 190 pruebas automatizadas, 24 de ellas específicas de seguridad, y alcanza una cobertura total del 74,04 %. El capítulo 36 documenta además seis comprobaciones funcionales de sistema.

## 38.3 Resultados y grado de cumplimiento

Los resultados muestran que se ha construido un prototipo funcional capaz de recorrer los principales flujos de diagnóstico y experimentación. Las pruebas de sistema del capítulo 36 documentan la carga de radiografías, la obtención de diagnósticos, la consulta del historial, el lanzamiento de entrenamientos, la consulta de resultados, la gestión de la cola, la supervisión administrativa y el cambio de idioma y tema.

La evidencia experimental disponible es más limitada que la capacidad prevista por el diseño. Se conservan resultados de ocho arquitecturas CNN, con cinco folds para cada una, pero no resultados equivalentes de las tres arquitecturas Transformer ni del resto de CNN previstas. Por tanto, el sistema demuestra la capacidad de ejecutar y organizar el pipeline, pero no permite establecer un ranking completo de todas las arquitecturas ni afirmar que una familia de modelos sea superior a otra.

La validación externa y el análisis estadístico están implementados como parte del laboratorio, aunque sus resultados deben interpretarse según la sesión ejecutada, el conjunto de datos utilizado y las diferencias entre las poblaciones. Las métricas de explicabilidad y calibración aportan información complementaria sobre el comportamiento de los modelos, pero no demuestran por sí solas fidelidad clínica, causalidad ni utilidad asistencial.

## 38.4 Limitaciones y conclusión final

El proyecto no constituye un producto sanitario ni un sistema preparado para sustituir la valoración de un profesional. No se ha realizado una evaluación clínica, una prueba formal de usabilidad con usuarios reales ni una validación completa de rendimiento. También permanecen pendientes pruebas de integración adicionales, entre ellas la comprobación de aislamiento entre usuarios, pruebas de rendimiento y verificaciones de recuperación de trabajos tras un reinicio.

La plataforma presupone que las imágenes introducidas por los usuarios han sido anonimizadas, pero no puede comprobarlo automáticamente. Además, la persistencia de las sesiones y de sus resultados en el sistema de ficheros requiere reforzar el aislamiento lógico, los controles de autorización y la protección de las rutas de los artefactos antes de un uso compartido o productivo. Estas limitaciones, junto con el marco regulatorio descrito en los capítulos 9 y 11, deben resolverse antes de plantear una evolución del sistema.

En conclusión, vitalXAI cumple como prototipo académico y entorno experimental integrado. Su valor principal no reside en proporcionar un diagnóstico clínico definitivo, sino en ofrecer una base operativa para estudiar modelos, explicaciones y procedimientos de evaluación de forma trazable y accesible. El trabajo futuro deberá ampliar el benchmarking, completar la verificación, reforzar la seguridad y evaluar el sistema en condiciones de uso representativas antes de considerar cualquier aplicación real.
