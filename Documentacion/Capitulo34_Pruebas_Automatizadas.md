# Capítulo 34: Pruebas automatizadas

Las pruebas automatizadas constituyen el primer nivel de la verificación de vitalXAI: comprueban el comportamiento de los componentes y de los flujos entre subsistemas de forma repetible, sin depender del entorno real de despliegue. Este capítulo describe las pruebas automatizadas del proyecto y presenta los resultados reales de su ejecución: las pruebas unitarias de los componentes, las pruebas de integración de los flujos entre subsistemas, la ejecución de la batería con las comprobaciones estáticas y la cobertura de los módulos de la aplicación. La distinción entre pruebas aisladas y pruebas de colaboración sigue la terminología habitual de la verificación de software (Myers, Sandler, & Badgett, 2011), y estas pruebas se corresponden con las categorías del plan de pruebas del capítulo 16.

La batería automatizada se ejecuta con pytest y pytest-cov, y se organiza en los directorios `tests/unit/` y `tests/integration/` del repositorio (pytest, 2024). Las pruebas unitarias sustituyen la base de datos, los modelos de TensorFlow y las dependencias externas por dobles de prueba, de modo que no dependen de la red ni de los pesos reales; las pruebas de integración utilizan una base de datos SQLite en memoria y comprueban principalmente los flujos de autenticación e historial.

## 34.1 Las pruebas unitarias

Las pruebas unitarias verifican el comportamiento de los componentes del sistema de manera aislada, organizadas por subsistema conforme a la estructura del capítulo 16. El conjunto comprende 186 pruebas distribuidas en 19 ficheros del directorio `tests/unit/`, que cubren los servicios y los enrutadores del backend: la gestión de cuentas y sesiones, la validación de las entradas, el motor de inferencia, la generación de las explicaciones, la gestión del historial, el laboratorio de entrenamiento, la cola de trabajos, la internacionalización y la capa de acceso a datos. La tabla siguiente desglosa las pruebas unitarias por fichero, agrupadas por subsistema.

| Subsistema | Fichero de pruebas | Nº de pruebas |
|---|---|---|
| Laboratorio MLOps | `test_trainer_router.py` | 30 |
| Acceso y gestión de cuentas | `test_auth_router.py` | 15 |
| Laboratorio MLOps | `test_trainer_engine.py` | 14 |
| Motor de diagnóstico | `test_xai_generator.py` | 13 |
| Capacidades transversales | `test_lang.py` | 12 |
| Laboratorio MLOps | `test_mlops_engine.py` | 11 |
| Motor de diagnóstico | `test_ml_engine.py` | 11 |
| Capacidades transversales | `test_queue_worker.py` | 10 |
| Supervisión y administración | `test_admin_router.py` | 10 |
| Acceso y gestión de cuentas | `test_auth_service.py` | 10 |
| Historial | `test_history_router.py` | 9 |
| Acceso y gestión de cuentas | `test_input_validation.py` | 8 |
| Seguridad | `test_security_headers.py` | 7 |
| Persistencia | `test_database.py` | 6 |
| Capacidades transversales | `test_queue_router.py` | 6 |
| Seguridad | `test_csrf_middleware.py` | 5 |
| Motor de diagnóstico | `test_pdf_generator.py` | 4 |
| Motor de diagnóstico | `test_inference_router.py` | 3 |
| Seguridad | `test_rate_limiting.py` | 2 |

La distribución de las pruebas refleja la complejidad funcional de cada subsistema: el laboratorio MLOps concentra el mayor número de verificaciones, por ser el bloque de mayor complejidad, seguido del acceso y la gestión de cuentas y del motor de diagnóstico. Las pruebas de cada fichero materializan las verificaciones unitarias del plan de pruebas del capítulo 16, los códigos PU-001 a PU-037, y se ejecutan de forma aislada, con la base de datos, los modelos y los servicios externos sustituidos por dobles.

## 34.2 Las pruebas de integración

Las pruebas de integración verifican la colaboración entre las capas del sistema y entre los subsistemas, superando el aislamiento de las pruebas unitarias. El conjunto comprende cuatro pruebas distribuidas en el fichero `test_auth_flow.py` del directorio `tests/integration/`. Comprueban el registro de un usuario, el inicio de sesión con las credenciales registradas, el acceso al panel, la redirección de un usuario no autenticado y el historial vacío de un usuario nuevo. Utilizan una base de datos SQLite en memoria y se centran en la colaboración entre la API, la capa de negocio y la persistencia.

Las pruebas de integración materializan las verificaciones PI-001 a PI-003 del plan de pruebas del capítulo 16, cubriendo el comportamiento especificado en los casos de uso CU-001, CU-002 y CU-005. Las ampliaciones previstas del plan, que incluyen los flujos del diagnóstico, el aislamiento de datos, la supervisión administrativa y el laboratorio, requieren pruebas adicionales conforme a la estrategia de verificación del capítulo 25.

## 34.3 Ejecución y resultados de la batería

La ejecución de la batería completa de pruebas automatizadas produjo 190 pruebas superadas sin fallos, con una duración aproximada de un minuto y quince segundos. La batería comprende las 186 pruebas unitarias y las cuatro pruebas de integración descritas en los apartados anteriores. El análisis estático con ruff también se superó sin errores y mypy no encontró problemas en los módulos configurados; esta última comprobación se ejecuta por separado de CI (Ruff, 2024; Mypy, 2024). Estos resultados respaldan los componentes unitarios y el flujo de autenticación cubierto por las pruebas de integración, pero no permiten afirmar que se hayan satisfecho todos los criterios del nivel de integración: PI-004 a PI-007, incluido el aislamiento entre usuarios, permanecen pendientes.

La ejecución de la batería se integra en el flujo de integración continua del repositorio. El workflow configurado ejecuta Ruff y pytest con medición de cobertura en los eventos definidos para las ramas y las peticiones de cambios, conforme al flujo descrito en el capítulo 27. El resultado global de la batería se resume en la tabla siguiente.

| Verificación | Resultado |
|---|---|
| Pruebas unitarias | 186 pruebas superadas. |
| Pruebas de integración | 4 pruebas superadas. |
| Total de la batería | 190 pruebas superadas, sin fallos. |
| Análisis estático (ruff) | Todas las comprobaciones superadas. |
| Verificación de tipos (mypy) | Sin problemas en los módulos configurados. |

## 34.4 Cobertura de los módulos

La cobertura de los módulos de la aplicación se midió con pytest-cov sobre los paquetes de servicios, los routers y el módulo de persistencia, obteniendo una cobertura total del 74,04 %, por encima del umbral mínimo del setenta por ciento definido en la guía de pruebas del proyecto. La tabla siguiente desglosa la cobertura alcanzada por cada módulo de la aplicación.

| Módulo | Cobertura |
|---|---|
| `services/csrf_middleware.py` | 100 % |
| `services/lang.py` | 100 % |
| `services/rate_limiter.py` | 100 % |
| `routers/inference.py` | 96 % |
| `services/ml_engine.py` | 96 % |
| `routers/admin.py` | 95 % |
| `services/auth_service.py` | 94 % |
| `services/chatbot_service.py` | 92 % |
| `routers/auth.py` | 86 % |
| `routers/history.py` | 85 % |
| `routers/trainer.py` | 84 % |
| `services/xai_generator.py` | 80 % |
| `services/pdf_generator.py` | 79 % |
| `routers/queue.py` | 74 % |
| `services/trainer_engine.py` | 71 % |
| `services/pdf_generator_mlops.py` | 57 % |
| `services/queue_worker.py` | 48 % |
| `services/mlops_engine.py` | 41 % |
| **Total** | **74,04 %** |

La cobertura refleja la estrategia de verificación de la plataforma: los módulos de seguridad transversal alcanzan el cien por cien de cobertura, y los módulos del diagnóstico y del acceso presentan valores elevados. Los módulos del laboratorio y de la ejecución asíncrona presentan los valores más bajos, porque su lógica se resuelve en gran medida en los scripts del pipeline y en los procesos del worker, que las pruebas unitarias verifican de forma parcial mediante los dobles de prueba. La batería automatizada permite considerar respaldadas las comprobaciones ejecutadas, pero no cubre de extremo a extremo los flujos PI-004 a PI-007. Las pruebas de seguridad, que comparten esta batería, se presentan con detalle en el capítulo siguiente.
