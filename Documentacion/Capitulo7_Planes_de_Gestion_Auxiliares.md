# Capítulo 7: Planes de apoyo a la gestión del proyecto

Este capítulo reúne los planes de apoyo que complementan el marco de gestión descrito en el capítulo 4. Además de la metodología y de la organización del trabajo, el proyecto necesita procedimientos para gestionar la comunicación, revisar la calidad del producto y del proceso, y conservar de forma ordenada el código fuente y sus entregables. El capítulo se estructura en tres apartados dedicados a estas dimensiones.

## 7.1 Plan de Comunicación

La comunicación del proyecto se adapta a un desarrollo unipersonal. La planificación y la revisión de las iteraciones se realizan mediante el tablero y reuniones de seguimiento programadas según la fase y la disponibilidad del tutor, no mediante dieciocho ceremonias formales con dedicación presupuestada. En la práctica, hubo un par de reuniones durante la planificación inicial, reuniones más frecuentes durante el desarrollo activo y reuniones puntuales durante la fase de documentación. Las horas imputadas al tutor se concentran en las tareas 0.1 y 8.3; el resto de las comunicaciones y revisiones puntuales no se contabiliza como dedicación adicional en el apartado de costes.

Al margen de estos hitos formales, la sincronización operativa se realiza mediante el tablero Kanban, que muestra el estado del desarrollo, y el correo electrónico para la gestión logística. Las consultas técnicas con los asesores se organizan cuando la complejidad del trabajo lo requiere, especialmente durante la integración de los módulos XAI y la construcción de los pipelines algorítmicos.

## 7.2 Plan de Calidad

El aseguramiento de la calidad del sistema se organiza en cuatro líneas de actuación.

A nivel de pruebas, el código se somete a pruebas unitarias sobre los módulos de procesamiento y predicción, pruebas de integración sobre los flujos del sistema, pruebas de seguridad sobre la autenticación y el control de acceso, y pruebas de rendimiento sobre la inferencia, la ejecución asíncrona y el acceso concurrente. Estas comprobaciones se describen en el capítulo 16. El desarrollo se apoya además en el ciclo basado en especificaciones y guiado por pruebas (SDD/TDD) descrito en el capítulo 4. Las funcionalidades cubiertas por este ciclo disponen de pruebas automatizadas antes de integrarse.

Respecto a los estándares estructurales, el código Python sigue las convenciones de PEP 8, que se revisan mediante herramientas de análisis estático (van Rossum, Warsaw, & Coghlan, 2001; Python Software Foundation, 2024). Los scripts de entrenamiento y el backend mantienen separadas sus responsabilidades, y las funciones principales incluyen docstrings con información sobre su propósito, sus entradas y su retorno.

En cuanto a la automatización, el repositorio utiliza un flujo de integración continua (CI) mediante GitHub Actions. En los eventos configurados para `main` y `refactorizacion` se ejecutan las pruebas con pytest, el análisis de estilo con Ruff y la comprobación de que la cobertura no desciende por debajo del 70 % (pytest, 2024; Ruff, 2024). Estas comprobaciones sirven como control previo a la integración de cambios.

Finalmente, para mejorar la reproducibilidad de los experimentos frente a la variabilidad debida a la inicialización aleatoria, el código fija semillas en las librerías críticas (TensorFlow, NumPy y Python) y almacena las configuraciones de cada experimento en archivos JSON vinculados a la sesión de entrenamiento. Estas medidas facilitan la repetición y la trazabilidad de los resultados, pero no garantizan por sí solas un determinismo bit a bit: las operaciones concurrentes de la GPU, las versiones del software y otros factores del entorno pueden introducir pequeñas diferencias entre ejecuciones. Por ello, los resultados deben reproducirse bajo las mismas condiciones documentadas y compararse atendiendo a la variabilidad observada.

## 7.3 Plan de Gestión de la Configuración

El código fuente del proyecto se almacena en un repositorio de GitHub. La rama principal (`main`) contiene el estado integrado y el trabajo puede organizarse en ramas con nombres descriptivos, como `feature/xai-quantitative-metrics` o `feature/training-pipeline-cnn`. La incorporación de cambios a `main` puede realizarse mediante Pull Requests para ejecutar las validaciones de GitHub Actions antes de la integración. Los commits descriptivos y las copias externas del repositorio se utilizan como medidas de trazabilidad y recuperación cuando resultan necesarios.

El repositorio integra un archivo `.gitignore` que excluye del control de versiones los conjuntos de datos radiológicos, los pesos de los modelos entrenados (archivos `.keras` y `.h5`), los artefactos generados (radiografías subidas, PDF y mapas de calor) y los residuos del entorno de desarrollo, como las cachés de Python, los entornos virtuales y las configuraciones locales. Esta configuración evita almacenar datos sensibles y mantiene en el repositorio los elementos necesarios para reproducir el entorno.

Los estados estables del código pueden identificarse mediante commits o etiquetas de Git cuando sea necesario relacionarlos con un entregable o un punto concreto de la planificación. El repositorio no mantiene una política formal de versiones etiquetadas para cada Sprint.
