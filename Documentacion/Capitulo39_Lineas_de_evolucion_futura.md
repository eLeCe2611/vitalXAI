# Capítulo 39: Líneas de evolución futura de vitalXAI

Las conclusiones del capítulo anterior muestran que vitalXAI constituye un prototipo funcional y un entorno de experimentación, pero también que todavía existen varias líneas prioritarias para ampliar su evidencia, robustez y utilidad. El trabajo futuro debe priorizarse de forma progresiva, empezando por completar la evaluación experimental y la verificación técnica antes de plantear un uso en contextos reales.

## 39.1 Ampliación de la evaluación experimental

La primera línea de trabajo consiste en completar el banco de pruebas previsto. Deben ejecutarse las arquitecturas CNN que no cuentan con resultados conservados y las tres arquitecturas Transformer, manteniendo una configuración experimental documentada y comparable. También sería conveniente repetir los entrenamientos con varias semillas y conservar los artefactos, logs y configuraciones necesarios para estimar la variabilidad de los resultados.

La evaluación debería ampliarse con otras estrategias de balanceo, ajustes de hiperparámetros y análisis de sensibilidad. Las métricas de explicabilidad y calibración deberían calcularse sobre muestras más amplias y representativas. Los contrastes estadísticos tendrían que aplicarse con un protocolo adecuado a la dependencia entre pliegues y con correcciones por comparaciones múltiples, evitando interpretar un ranking exploratorio como una demostración de superioridad.

También debe completarse la validación externa con cohortes independientes y mejor caracterizadas. Sería recomendable incorporar conjuntos procedentes de distintos centros, equipos y protocolos de adquisición, controlar posibles señales asociadas al origen de las imágenes y estudiar el comportamiento de los modelos por subgrupos relevantes. Esta ampliación permitiría valorar mejor la generalización, aunque no sustituiría una validación clínica.

## 39.2 Evolución técnica y de seguridad

Una evolución prioritaria es reforzar el aislamiento de los datos del laboratorio. Las sesiones, resultados y artefactos deberían vincularse de forma persistente y verificable al usuario propietario, y esa propiedad debería comprobarse en todas las operaciones de consulta, descarga, renombrado y eliminación. Esta mejora debe acompañarse de pruebas de integración específicas que cubran el acceso cruzado entre usuarios y las funciones administrativas.

También deben completarse la recuperación idempotente de trabajos tras reinicios, la gestión de resultados parciales y las pruebas de rendimiento de la inferencia, la cola y el acceso concurrente. La limitación del número de entrenamientos simultáneos y encolados ayudaría a evitar que la competición por la GPU degrade el servicio. Asimismo, sería conveniente mejorar la auditoría de operaciones, la monitorización y la gestión de errores del laboratorio.

Desde el punto de vista de la protección de datos, el sistema debería incorporar la eliminación de metadatos identificables, la detección de información sensible y políticas explícitas de retención y borrado. Estas medidas no eliminan la responsabilidad del usuario sobre los datos introducidos, pero reducen el riesgo de almacenar información no anonimizada.

## 39.3 Validación con usuarios y contexto clínico

Antes de considerar un uso asistencial, debe realizarse una evaluación con facultativos, investigadores y otros perfiles representativos. Esta evaluación debería analizar la facilidad de aprendizaje, la claridad de los resultados, la comprensión de los mapas de explicabilidad, la utilidad de los informes y la carga de trabajo que introduce la plataforma.

También sería necesario estudiar cómo se integra la herramienta en un flujo de trabajo real y qué información necesita el profesional para interpretar correctamente una predicción. Las explicaciones visuales deberían revisarse junto con especialistas para determinar si son coherentes, estables y suficientemente comprensibles, sin asumir que una región resaltada constituye una justificación clínica válida.

## 39.4 Preparación para un despliegue real

Una fase posterior podría abordar la preparación de una versión más robusta para entornos compartidos o de demostración avanzada. Esto incluiría automatizar la construcción y el despliegue, separar los entornos de desarrollo y producción, gestionar de forma segura los secretos, establecer copias de seguridad y definir procedimientos de recuperación y mantenimiento.

Finalmente, cualquier transferencia a un entorno sanitario exigiría revisar la normativa aplicable, definir responsabilidades, documentar el uso previsto y realizar las evaluaciones técnicas, clínicas y organizativas correspondientes. Hasta completar estas etapas, vitalXAI debe mantenerse como una plataforma de investigación y apoyo, no como un sistema autónomo de diagnóstico.
