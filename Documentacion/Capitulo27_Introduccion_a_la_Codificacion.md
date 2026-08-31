# Capítulo 27: Introducción a la codificación

Esta parte de la memoria describe cómo se implementó vitalXAI a partir del diseño de los capítulos 17 a 26. El capítulo introductorio sitúa la organización del repositorio, las convenciones de código, las capas tecnológicas y las herramientas de calidad; los capítulos siguientes muestran las decisiones y los fragmentos más representativos de cada módulo. La implementación resultante es una aplicación Python servida por FastAPI, con persistencia en MySQL y un laboratorio MLOps basado en los servicios y scripts del proyecto.

La parte se organiza en seis capítulos. Este capítulo introductorio presenta la visión general de la implementación, la estructura del repositorio, las convenciones de código y las herramientas de calidad; los cinco capítulos siguientes describen la codificación de cada capa tecnológica: el backend (capítulo 28), la ejecución asíncrona (capítulo 29), el motor de diagnóstico y de explicabilidad (capítulo 30), el laboratorio de experimentación MLOps (capítulo 31) y el frontend (capítulo 32). Cada capítulo de codificación presenta los componentes implementados, los fragmentos de código representativos con su explicación y la coherencia con el diseño del sistema.

La implementación de vitalXAI se acompaña de una batería automatizada de pruebas unitarias y de integración, integrada en el flujo de integración continua. En el estado actual del repositorio se han ejecutado más de ciento ochenta pruebas; el plan del capítulo 16 define su alcance y sus criterios, pero esta cifra no implica que cada capacidad se desarrollara estrictamente mediante TDD (Myers, Sandler, & Badgett, 2011). Los capítulos siguientes describen la implementación real, con referencias a los módulos, los ficheros de pruebas y las decisiones técnicas que la sustentan.

## 27.1 Visión general de la implementación

La implementación de vitalXAI se organiza en torno a las capas definidas en el diseño: la capa HTTP, la capa de servicios, la persistencia relacional, la ejecución asíncrona, el motor de inteligencia artificial y la capa de presentación. La capa HTTP agrupa los routers que exponen los endpoints de la API; la capa de servicios concentra la lógica de aplicación, como criptografía, sesiones, predicción, explicabilidad, informes, laboratorio y cola; la persistencia relacional se resuelve con MySQL a través de un pool de conexiones; la ejecución asíncrona se materializa en la cola de trabajos y en el worker; el motor de inteligencia artificial agrupa la carga de los modelos y la generación de las explicaciones; y la capa de presentación se compone de las plantillas Jinja2 y los recursos JavaScript del navegador. Estas responsabilidades se distribuyen entre los directorios y módulos de la raíz, no en paquetes independientes para cada capa.

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

La estructura distingue los ficheros raíz de la aplicación, los paquetes de la implementación y los directorios de artefactos. Los ficheros raíz incluyen el punto de entrada `main.py`, la persistencia `database.py`, las dependencias `requirements.txt`, la configuración de calidad `pyproject.toml`, la configuración de la integración continua en `.github/workflows/` y las variables de entorno. Los directorios `routers/`, `services/`, `templates/` y `static/` contienen la implementación de cada capa; `pneumoniacnn-main/` alberga el pipeline de experimentación con sus scripts y los pesos de los modelos; `tests/` contiene las pruebas unitarias y de integración; `scripts/` reúne los scripts operativos de arranque y de migración; y `training_results/` junto con los subdirectorios de `static/` conserva los artefactos generados y los recursos de la aplicación.

## 27.3 Convenciones de código y decisiones transversales

La codificación de vitalXAI toma como referencia las convenciones de estilo de Python de PEP 8 (van Rossum, Warsaw, & Coghlan, 2001). Ruff revisa automáticamente el conjunto de reglas seleccionado por el proyecto, que incluye errores sintácticos, advertencias, importaciones, convenciones de nombres, actualizaciones de sintaxis, comprobaciones de seguridad y simplificaciones. La configuración fija una longitud máxima de línea de 140 caracteres y estas comprobaciones se ejecutan en el flujo de integración; esto ayuda a mantener un estilo uniforme, pero no equivale por sí solo a una conformidad completa con PEP 8.

Las decisiones transversales de codificación incluyen el uso de anotaciones de tipos, la política de comentarios y la gestión de los recursos. El proyecto emplea anotaciones en los módulos de mayor criticidad, especialmente los servicios de autenticación y seguridad, y dispone de una configuración de mypy para comprobar esos módulos cuando se ejecuta la herramienta. Los comentarios se reservan para explicar la intención y las decisiones no evidentes de cada bloque, sin narrar la mecánica obvia del código. Las variables de entorno se leen mediante la función de carga del entorno, de modo que la configuración sensible permanece fuera del código y se suministra en tiempo de ejecución. Los identificadores de los módulos y de las funciones siguen las convenciones de nombres de Python, con módulos en minúsculas separados por guiones bajos y funciones con la misma convención.

## 27.4 Herramientas y calidad del código

La calidad del código de vitalXAI se comprueba mediante herramientas integradas en el flujo de trabajo. pytest ejecuta las pruebas unitarias y de integración y pytest-cov mide la cobertura de los módulos de la aplicación; los dobles de prueba se construyen principalmente con `unittest.mock` y fixtures de pytest (pytest, 2024). La cobertura está sujeta a un umbral mínimo del setenta por ciento, de modo que la configuración de CI hace fallar la batería si no se alcanza. Ruff comprueba el estilo y las reglas del código (Ruff, 2024), mientras que mypy dispone de una configuración para la verificación de tipos, aunque no se ejecuta actualmente en CI (Mypy, 2024).

La verificación se integra en la integración continua mediante el workflow del repositorio, que se ejecuta en los eventos configurados para las ramas principales y las peticiones de cambios. El workflow instala las dependencias, ejecuta Ruff y ejecuta pytest con medición de cobertura. De este modo se comprueban automáticamente el comportamiento cubierto por las pruebas, el estilo y el umbral de cobertura; la verificación de tipos requiere ejecutar mypy por separado. Esta estrategia es coherente con la estrategia de verificación del capítulo 25, aunque no permite afirmar que toda la implementación esté verificada.
