# Capítulo 35: Pruebas de seguridad

Este capítulo presenta la evidencia automatizada obtenida para los mecanismos de seguridad implementados en vitalXAI. El alcance cubre la protección CSRF, las cabeceras de seguridad, la limitación de peticiones y el ciclo de vida de los tokens de sesión, controles relacionados con riesgos habituales de las aplicaciones web autenticadas (OWASP, 2024). Las pruebas se corresponden con la categoría de protección y control de acceso del plan de pruebas del capítulo 16, concretamente con los códigos PS-001 a PS-009, y forman parte de la batería descrita en el capítulo 34.

Las pruebas de seguridad se implementan en los ficheros `test_csrf_middleware.py`, `test_security_headers.py`, `test_rate_limiting.py` y `test_auth_service.py` del directorio `tests/unit/`, y se ejecutan de forma aislada, sin dependencia del entorno real, verificando los mecanismos de seguridad implementados en el backend descrito en el capítulo 28. La ejecución específica de estos ficheros produjo un resultado de 24 pruebas superadas sin fallos, como se detalla en cada apartado.

## 35.1 Protección CSRF

La protección CSRF se verifica con las cinco pruebas del fichero `test_csrf_middleware.py`, que comprueban el comportamiento del middleware de protección frente a las peticiones que modifican el estado. Las pruebas cubren los casos PS-001 a PS-004 del plan: el rechazo de una petición POST sin token CSRF, el procesamiento de una petición POST con un token válido, el rechazo de una petición POST con un token erróneo y la exención de las peticiones GET de la protección. La tabla siguiente desglosa estas verificaciones.

| ID | Verificación | Resultado |
|---|---|---|
| PS-001 | Una petición POST sin token CSRF es rechazada. | Superada. |
| PS-002 | Una petición POST con token CSRF válido se procesa. | Superada. |
| PS-003 | Una petición POST con token CSRF erróneo es rechazada. | Superada. |
| PS-004 | Las peticiones GET están exentas de la protección CSRF. | Superada. |

Las verificaciones confirman que el middleware implementado en `csrf_middleware.py` establece la cookie del token en las peticiones seguras y exige su correspondencia con la cabecera en las peticiones que modifican el estado, de modo que una petición de modificación sin el token o con un token erróneo responde HTTP 403 sin procesarse, tal y como se describió en la codificación del backend.

## 35.2 Cabeceras de seguridad

Las cabeceras de seguridad se verifican con las siete pruebas del fichero `test_security_headers.py`, que comprueban que todas las respuestas de la aplicación incluyen las cabeceras configuradas. Las pruebas cubren los casos PS-005 a PS-007 del plan y las cabeceras complementarias: la política de seguridad de contenido (Content-Security-Policy), la seguridad de transporte (Strict-Transport-Security), la opción de tipo de contenido (X-Content-Type-Options), el marco (X-Frame-Options), la protección de XSS y la política de referente. La tabla siguiente resume las verificaciones principales.

| ID | Verificación | Resultado |
|---|---|---|
| PS-005 | Las respuestas incluyen la cabecera Content-Security-Policy. | Superada. |
| PS-006 | Las respuestas incluyen la cabecera Strict-Transport-Security. | Superada. |
| PS-007 | Las respuestas incluyen la cabecera X-Content-Type-Options. | Superada. |

Las verificaciones confirman que el middleware de cabeceras de seguridad añade las cabeceras configuradas a todas las respuestas de la aplicación, en coherencia con las directivas definidas en la codificación del backend, de modo que el navegador aplica las restricciones de contenido, transporte y tipo MIME en cada respuesta.

## 35.3 Limitación de peticiones

La limitación de peticiones se verifica con las dos pruebas del fichero `test_rate_limiting.py`, que comprueban el comportamiento del limitador configurado en el backend. Las pruebas cubren la limitación del endpoint de inicio de sesión, que permite cinco peticiones por minuto, verificando que la sexta petición en el mismo minuto es rechazada, y la aplicación de la limitación global sobre las peticiones de la aplicación. La tabla siguiente resume estas verificaciones.

| ID | Verificación | Resultado |
|---|---|---|
| PS-008 | El inicio de sesión está limitado en frecuencia. | Superada. |

La verificación confirma que el limitador implementado en `rate_limiter.py` rechaza los intentos reiterados de acceso desde una misma dirección, en coherencia con el requisito de protección frente a ataques de fuerza bruta y con la codificación del backend descrita en el capítulo 28.

## 35.4 Gestión de los tokens de sesión

La gestión de los tokens de sesión se verifica con las diez pruebas del fichero `test_auth_service.py`, que comprueban el comportamiento del servicio de autenticación respecto a las credenciales y a los tokens. Las pruebas cubren la creación y la verificación de los tokens de acceso, la creación y la verificación de los tokens de refresco, la invalidación de los tokens revocados, la rotación del token de refresco y la detección del robo de sesión. Entre ellas se encuentra la verificación PS-009 del plan, que comprueba que el acceso con un token de refresco revocado es rechazado. La tabla siguiente resume las verificaciones principales.

| ID | Verificación | Resultado |
|---|---|---|
| PS-009 | El acceso con un token de refresco revocado es rechazado. | Superada. |
| N/A | La rotación del token de refresco invalida el anterior. | Superada. |
| N/A | La detección de robo de sesión revoca todos los tokens del usuario. | Superada. |

Las verificaciones confirman que el servicio de autenticación implementado en `auth_service.py` gestiona correctamente el ciclo de vida de los tokens: la verificación distingue el token activo, el revocado dentro del periodo de gracia y el uso de una credencial revocada, y ante este último revoca todos los tokens del usuario, tal y como se describió en la codificación del backend y en el diseño del subsistema de acceso.

## 35.5 Resultados de la verificación de seguridad

La ejecución específica de las pruebas de seguridad produjo un resultado de 24 pruebas superadas sin fallos, distribuidas en los cuatro ficheros de verificación. La tabla siguiente resume el resultado de la verificación de seguridad.

| Fichero de pruebas | Verificaciones | Resultado |
|---|---|---|
| `test_csrf_middleware.py` | 5 | Superadas. |
| `test_security_headers.py` | 7 | Superadas. |
| `test_rate_limiting.py` | 2 | Superadas. |
| `test_auth_service.py` | 10 | Superadas. |
| **Total** | **24** | **Superadas.** |

Las verificaciones de seguridad confirman el funcionamiento de los mecanismos evaluados: la protección frente a la falsificación de peticiones en sitios cruzados, las cabeceras de seguridad, la limitación de los intentos de acceso y la gestión de las credenciales de sesión. Estos resultados no equivalen a una certificación de seguridad completa ni cubren los controles pendientes de auditoría, protección de datos y despliegue; tampoco sustituyen una evaluación de amenazas más amplia basada en el contexto de operación (OWASP, 2024). La verificación en el entorno real, junto con las pruebas de rendimiento y de los flujos completos, se describe en los capítulos siguientes de la parte de verificación.
