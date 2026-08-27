# Capítulo 27: Introducción a la codificación

La parte de codificación de la memoria describe la implementación del sistema vitalXAI: cómo se materializó en código ejecutable el diseño especificado en los capítulos 17 a 26. Mientras que el diseño determina la arquitectura, los casos de uso, las clases, las interfaces, la construcción, la preparación de los datos, la verificación y la implantación, esta parte describe las decisiones de implementación concretas que hicieron realidad el sistema: la organización del repositorio, las convenciones de código, la estructura de cada capa tecnológica y los fragmentos de código más representativos de cada módulo. La codificación es, por tanto, la traducción fiel del diseño a un sistema Python servido por FastAPI y apoyado en MySQL, TensorFlow y los servicios del laboratorio MLOps.

La parte se organiza en seis capítulos. Este capítulo introductorio presenta la visión general de la implementación, la estructura del repositorio, las convenciones de código y las herramientas de calidad; los cinco capítulos siguientes describen la codificación de cada capa tecnológica: el backend (capítulo 28), la ejecución asíncrona (capítulo 29), el motor de diagnóstico y de explicabilidad (capítulo 30), el laboratorio de experimentación MLOps (capítulo 31) y el frontend (capítulo 32). Cada capítulo de codificación presenta los componentes implementados, los fragmentos de código representativos con su explicación y la coherencia con el diseño del sistema.

La codificación de vitalXAI siguió la metodología de desarrollo dirigida por pruebas (TDD) declarada en el plan de pruebas del capítulo 16, de modo que cada capacidad funcional se implementó después de escribir la prueba que verifica su comportamiento. Esta metodología dio lugar a una batería de pruebas automatizadas —más de ciento ochenta pruebas distribuidas entre unitarias y de integración— que acompaña a la implementación y que se integra en el flujo de integración continua (Myers, Sandler, & Badgett, 2011). Los capítulos siguientes describen la implementación real del sistema, referenciando los módulos, los ficheros de pruebas y las decisiones técnicas que la sustentan.

## 27.1 Visión general de la implementación

La implementación de vitalXAI se organiza en torno a las capas definidas en el diseño: la capa HTTP, la capa de servicios, la persistencia relacional, la ejecución asíncrona, el motor de inteligencia artificial y la capa de presentación. La capa HTTP agrupa los routers que exponen los endpoints de la API; la capa de servicios concentra la lógica de aplicación —criptografía, sesiones, predicción, explicabilidad, informes, laboratorio y cola—; la persistencia relacional se resuelve con MySQL a través de un pool de conexiones; la ejecución asíncrona se materializa en la cola de trabajos y en el worker; el motor de inteligencia artificial agrupa la carga de los modelos y la generación de las explicaciones; y la capa de presentación se compone de las plantillas Jinja2 y los recursos JavaScript del navegador. Cada capa se implementa en un paquete del repositorio, de modo que la estructura del código refleja la arquitectura del sistema.

El lenguaje de implementación es Python en su versión 3.11, que alberga tanto el servidor web como el motor de aprendizaje profundo. El servidor se construye con FastAPI y se sirve mediante Uvicorn; las plantillas se componen con Jinja2; la persistencia se accede mediante el conector MySQL de Python; el aprendizaje profundo se apoya en TensorFlow y en la librería Transformers de Hugging Face; y la seguridad de las sesiones se resuelve con bcrypt, python-jose y slowapi. Estas tecnologías, junto con el resto de las dependencias del sistema, se describieron en el entorno de construcción del capítulo 23, y su implementación se detalla en los capítulos de codificación de esta parte.

La coherencia entre el diseño y la implementación se mantiene mediante la trazabilidad de los módulos: cada router y cada servicio del código se corresponde con los componentes descritos en el capítulo 17 y con las clases de diseño del capítulo 21, y cada endpoint materializa los casos de uso del capítulo 20. Esta correspondencia permite verificar que la implementación satisface el diseño y que los capítulos de codificación pueden leerse como la materialización concreta de las decisiones técnicas ya documentadas.

## 27.2 Estructura del repositorio

La estructura del repositorio del proyecto refleja la organización por capas de la implementación. El árbol de directorios de la figura 104 representa la estructura del repositorio de vitalXAI y los ficheros principales de cada paquete, con sus agrupaciones funcionales.

```
vitalXAI/
├── .github/
│   └── workflows/
│       └── ci.yml
├── routers/
│   ├── admin.py
│   ├── auth.py
│   ├── history.py
│   ├── inference.py
│   ├── queue.py
│   └── trainer.py
├── services/
│   ├── auth_service.py
│   ├── chatbot_service.py
│   ├── csrf_middleware.py
│   ├── lang.py
│   ├── ml_engine.py
│   ├── mlops_engine.py
│   ├── pdf_generator.py
│   ├── pdf_generator_mlops.py
│   ├── queue_worker.py
│   ├── rate_limiter.py
│   ├── trainer_engine.py
│   └── xai_generator.py
├── static/
│   ├── js/
│   │   ├── admin.js
│   │   ├── dashboard.js
│   │   ├── i18n.js
│   │   └── training.js
│   ├── uploads/
│   ├── results/
│   └── reports/
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── training.html
├── tests/
│   ├── unit/
│   └── integration/
├── pneumoniacnn-main/
│   ├── code/
│   │   ├── 1_train_kfold.py
│   │   ├── 2_train_transformer_kfold.py
│   │   ├── 3_evaluate_statistics.py
│   │   ├── 4_external_validation.py
│   │   ├── 5_evaluate_delong.py
│   │   ├── 6_xai_qualitative.py
│   │   └── 7_xai_quantitative.py
│   └── results/
├── scripts/
│   ├── demo_start.bat
│   ├── demo_start.ps1
│   ├── migrate_passwords.py
│   └── migrate_roles.py
├── sql/
├── training_results/
├── .env.example
├── .gitignore
├── database.py
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

*Figura 104 - Estructura del repositorio de vitalXAI*

La estructura distingue los ficheros raíz de la aplicación, los paquetes de la implementación y los directorios de artefactos. Los ficheros raíz incluyen el punto de entrada `main.py`, la persistencia `database.py`, las dependencias `requirements.txt`, la configuración de calidad `pyproject.toml`, la configuración de la integración continua en `.github/workflows/` y las variables de entorno. Los paquetes `routers/`, `services/`, `templates/` y `static/` contienen la implementación de cada capa; el directorio `pneumoniacnn-main/` alberga el pipeline de experimentación con sus scripts y los pesos de los modelos; el directorio `tests/` contiene las pruebas unitarias y de integración; el directorio `scripts/` reúne los scripts operativos de arranque y de migración; y los directorios `sql/`, `training_results/` y los subdirectorios de `static/` conservan los artefactos generados y los recursos de la aplicación.

## 27.3 Convenciones de código y decisiones transversales

La codificación de vitalXAI sigue las convenciones de estilo de Python definidas en la guía de estilo PEP 8 (van Rossum, Warsaw, & Coghlan, 2001), aplicadas de forma automática por la herramienta de análisis estático ruff. La configuración del proyecto fija una longitud máxima de línea de 140 caracteres y la selección de un conjunto de reglas que abarca los errores sintácticos, las advertencias, las importaciones, las convenciones de nombres, las actualizaciones de sintaxis, las comprobaciones de seguridad y las mejoras de simplificación. La aplicación de estas reglas se verifica de forma continua en el flujo de integración, de modo que el estilo del código se mantiene consistente en todo el repositorio.

Las decisiones transversales de codificación incluyen el uso de tipos estáticos, la política de comentarios y la gestión de los recursos. El proyecto emplea anotaciones de tipos en los módulos de mayor criticidad —los servicios de autenticación y seguridad—, verificadas con la herramienta mypy, de modo que las funciones documentan sus parámetros y sus valores de retorno y los errores de tipos se detectan en tiempo de verificación. Los comentarios se reservan para explicar la intención y las decisiones no evidentes de cada bloque, sin narrar la mecánica obvia del código, en línea con las prácticas de calidad del proyecto. Las variables de entorno se leen mediante la función de carga del entorno, de modo que la configuración sensible permanece fuera del código y se suministra en tiempo de ejecución. Los identificadores de los módulos y de las funciones siguen las convenciones de nombres de Python, con módulos en minúsculas separados por guiones bajos y funciones con la misma convención.

## 27.4 Herramientas y calidad del código

La calidad del código de vitalXAI se garantiza mediante un conjunto de herramientas de verificación integradas en el flujo de trabajo. El marco de pruebas pytest ejecuta la batería de pruebas unitarias y de integración, con la extensión pytest-cov para medir la cobertura de los módulos de la aplicación y la extensión pytest-mock para la simulación de los servicios externos (pytest, 2024). La cobertura de los módulos de la aplicación está sujeta a un umbral mínimo del setenta por ciento, de modo que la batería falla si la cobertura desciende por debajo del umbral. El análisis estático del estilo y de las reglas se resuelve con ruff (Ruff, 2024), y la verificación de tipos se resuelve con mypy en los módulos de seguridad configurados (Mypy, 2024).

La verificación se integra en la integración continua mediante el flujo de trabajo del repositorio, que se ejecuta en cada integración de la rama principal y en cada petición de cambios. El flujo instala las dependencias, ejecuta el análisis estático con ruff y ejecuta la batería de pruebas con la medición de cobertura, de modo que cualquier regresión de comportamiento, de estilo o de tipos se detecta de forma inmediata. Esta estrategia, coherente con la definida en la estrategia de verificación del sistema del capítulo 25, garantiza que la codificación se mantiene estable a lo largo del desarrollo y que los capítulos siguientes describen una implementación verificada y mantenible.
