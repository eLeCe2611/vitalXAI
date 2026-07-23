# Capítulo 7: Planes de gestión auxiliares

## Plan de Comunicación

La comunicación del proyecto sigue la cadencia natural de Scrum. Al inicio de cada Sprint, se realizará una reunión de Sprint Planning en la que el tutor y el alumno acordarán los objetivos, las tareas a abordar y la estimación del esfuerzo. Cuando finalice el Sprint se realizará una reunión de Sprint Review en la que se presentarán los incrementos completados y se validarán frente a los criterios de aceptación que han sido definidos.

Sin tener en cuenta estas reuniones formales, la comunicación se realizará de manera asíncrona a través del tablero Kanban del proyecto, que refleja en todo momento el estado actualizado de las tareas, y del correo electrónico para la coordinación puntual de fechas o la resolución de dudas. Las consultas técnicas con los asesores se realizarán mediante reuniones específicas convocadas cuando el avance del Sprint así lo requiera, particularmente en los Sprints de implementación de los módulos XAI y los pipelines de entrenamiento.

## Plan de Calidad

La calidad del sistema se garantizará a través de cuatro líneas de actuación complementarias.

Desde el punto de vista de las pruebas, se realizarán pruebas unitarias sobre los módulos de procesamiento de imagen y predicción, pruebas de integración sobre el flujo completo de diagnóstico (subida de imagen, inferencia, generación XAI y descarga de PDF), pruebas de seguridad sobre los mecanismos de autenticación y acceso a datos, y pruebas de rendimiento sobre los pipelines de entrenamiento para verificar que los tiempos de ejecución se mantienen dentro de los márgenes planificados.

En cuanto a los estándares de código, todo el código Python seguirá las convenciones de estilo PEP 8, verificándose su cumplimiento mediante herramientas de análisis estático. Los scripts de entrenamiento y los módulos del backend mantendrán una separación clara de responsabilidades, con funciones documentadas mediante docstrings que describan su propósito, parámetros y valor de retorno.

En cuanto a la automatización, se configurará un flujo de integración continua mediante GitHub Actions que ejecutará de manera automática las comprobaciones de estilo y los tests unitarios en cada Pull Request que se realice, garantizando que ningún código que no pase las validaciones pueda integrarse en la rama principal.

En cuanto a la reproducibilidad de los resultados, dado que el entrenamiento de modelos de deep learning puede introducir variabilidad debida a la inicialización aleatoria de los pesos, al orden de procesamiento de los datos y a la plataforma hardware subyacente, se fijarán semillas aleatorias en todas las librerías involucradas (TensorFlow, NumPy, Python random) para garantizar que los experimentos sean reproducibles bajo las mismas condiciones. Además, se almacenarán las configuraciones completas de cada experimento en archivos JSON asociados a cada sesión de entrenamiento, permitiendo la trazabilidad completa de los resultados.

## Plan de Gestión de la Configuración

Todo el código del proyecto se mantendrá alojado en un repositorio privado en GitHub. El flujo de trabajo que se adopta en el proyecto es GitHub Flow, que define una rama principal `main` que siempre contiene código estable y desplegable, y para cada nueva funcionalidad o tarea se crea una rama de corta duración con un nombre descriptivo, por ejemplo, `feature/xai-quantitative-metrics` o `feature/training-pipeline-cnn`. La integración en la rama `main` se realizará de manera exclusiva a través de Pull Requests, incluso si se está trabajando en solitario, lo que permite disparar automáticamente los flujos de GitHub Actions antes de fusionar.

El repositorio incluirá un archivo `.gitignore` configurado para excluir del control de versiones los elementos que no deben ser trackeados: los datasets de imágenes médicas (rayos X), los pesos de los modelos entrenados (archivos `.keras`, `.h5`), los archivos generados por los usuarios (radiografías subidas, informes PDF, mapas XAI) y los artefactos propios del entorno de desarrollo (cachés de Python, entornos virtuales, archivos de configuración local). Esta configuración garantiza que el repositorio contenga únicamente el código fuente, la documentación y los archivos de configuración necesarios para reproducir el entorno, manteniendo un tamaño de repositorio manejable y evitando la exposición de datos sensibles.

El versionado de entregas seguirá el estándar Semantic Versioning (SemVer), que define la versión como MAJOR.MINOR.PATCH, etiquetando cada entrega al cierre del Sprint mediante tags de Git, por ejemplo, `v1.3.0`. Las etiquetas permitirán identificar de manera inequívoca el estado del proyecto en cada hito de la planificación.
