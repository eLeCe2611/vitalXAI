# Capítulo 18: Arquitectura de soporte y mecanismos transversales

La arquitectura de soporte reúne los elementos que permiten que los subsistemas funcionales operen de forma coordinada, segura y mantenible. A diferencia de los subsistemas de diseño del capítulo 17, estos componentes no representan una capacidad clínica o investigadora concreta para el usuario. Su responsabilidad es proporcionar persistencia, almacenamiento, configuración, protección, validación y ejecución común a las funcionalidades de autenticación, diagnóstico, historial, laboratorio y administración (Larman, 2004; Jacobson, Booch & Rumbaugh, 1999).

La separación entre funcionalidad y soporte no significa que ambos ámbitos estén desconectados. SD-002 depende del almacenamiento y de la cola; SD-004 necesita el sistema de ficheros, MySQL y la configuración de los servicios externos; SD-001 utiliza el middleware de seguridad; y todos los routers dependen del ciclo de vida de FastAPI. La arquitectura de soporte permite que estas dependencias se apliquen de forma uniforme, evitando que cada módulo implemente su propia conexión, su propio control de errores o su propia interpretación del entorno.

En la implementación actual se distinguen dos dimensiones. La primera está formada por los subsistemas de soporte, que agrupan servicios o recursos con una identidad técnica propia: persistencia relacional, almacenamiento de ficheros, entorno de ejecución e integración externa y calidad operativa. La segunda está formada por los mecanismos de diseño transversales, que son reglas aplicadas a varios componentes: gestión de configuración, validación de entradas, autenticación y autorización, manejo de errores, ejecución asíncrona, modularidad y pruebas automatizadas.

### 18.1 Subsistemas de soporte

Los subsistemas de soporte descritos en esta sección no sustituyen a SD-006 ni duplican sus responsabilidades. SD-006 pertenece a la lógica de capacidades transversales que el usuario puede utilizar, como consultar o cancelar un trabajo. En cambio, los subsistemas de soporte proporcionan la infraestructura que hace posible esa capacidad: la conexión a MySQL, el sistema de ficheros, el entorno de ejecución y los servicios que se integran con la plataforma.

| Subsistema de soporte | Responsabilidad | Componentes actuales |
|---|---|---|
| SSOP-001 Persistencia relacional | Crear conexiones, conservar entidades y asegurar la integridad básica de las relaciones. | `database.py`, `MySQLConnectionPool`, MySQL/XAMPP y tablas del esquema. |
| SSOP-002 Almacenamiento de ficheros y recursos | Conservar imágenes, mapas XAI, informes, resultados MLOps, plantillas y recursos estáticos. | `static/`, `templates/`, `training_results/` y montajes de `main.py`. |
| SSOP-003 Entorno de ejecución e integración | Proporcionar el proceso web, las dependencias Python y el acceso a APIs y repositorios externos. | Uvicorn, FastAPI, entorno virtual, Groq, Hugging Face y variables de entorno. |
| SSOP-004 Calidad y verificación | Comprobar el comportamiento de los componentes y detectar regresiones durante el desarrollo. | pytest, fixtures de `tests/conftest.py`, mocks, pytest-cov, ruff y CI. |

*Tabla 51 - Subsistemas de soporte de vitalXAI*

#### 18.1.1 SSOP-001: Persistencia relacional y conexiones de base de datos

El subsistema SSOP-001 encapsula el acceso de la aplicación a MySQL. Su componente principal es `database.py`, que mantiene una referencia al pool de conexiones y expone `get_db_connection()` para que los routers y servicios puedan solicitar una conexión sin conocer cómo se crea. La configuración se obtiene de `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` y `DB_POOL_SIZE`, con valores de desarrollo definidos cuando el entorno no proporciona una variable concreta.

El pool se crea de forma diferida. La primera operación que necesita una conexión invoca `_get_pool()`, que construye un `MySQLConnectionPool` con el tamaño configurado. Las operaciones posteriores reutilizan el mismo objeto y solicitan conexiones disponibles mediante `get_connection()`. Este comportamiento reduce el coste de crear conexiones repetidas y proporciona un punto único desde el que controlar el acceso concurrente a la base de datos.

La inicialización del esquema se realiza mediante `init_db()`, llamada durante el `lifespan` de FastAPI. El procedimiento comprueba la existencia de las tablas `users`, `consultations`, `training_jobs`, `job_queue` y `refresh_tokens`, y crea las que no existan. Esta estrategia es adecuada para el entorno local y de demostración actual, donde la base de datos se inicializa desde la aplicación. No equivale a un sistema de migraciones versionadas: una evolución posterior del esquema deberá gestionarse con un procedimiento controlado para no depender únicamente de sentencias `CREATE TABLE IF NOT EXISTS`.

La persistencia relacional cumple dos funciones diferentes. Por un lado, conserva información de negocio, como las cuentas y consultas. Por otro, sirve de soporte operacional para la cola de trabajos y los tokens de refresco. En ambos casos se utilizan consultas parametrizadas, se confirma la escritura con `commit()` y se cierra la conexión tras terminar. Las claves ajenas de las tablas de trabajos, consultas y tokens apuntan a `users`, lo que mantiene la relación de propiedad a nivel de esquema.

Los componentes funcionales no comparten una conexión global abierta. Cada router o servicio solicita una conexión para una operación concreta, obtiene un cursor, ejecuta la consulta y cierra la conexión. Esta decisión limita el alcance de un error de conexión y evita que una petición retenga indefinidamente un recurso del pool. El coste de esta estrategia se controla mediante `DB_POOL_SIZE`, que debe ajustarse a la capacidad real de MySQL y al número de peticiones que se espera atender.

El subsistema también define el comportamiento ante indisponibilidad. Si MySQL no puede conectarse durante el arranque, `main.py` muestra un aviso operativo indicando que debe iniciarse XAMPP o revisarse la configuración. La aplicación puede continuar hasta iniciar el worker, pero las operaciones que requieren identidad, persistencia o cola no podrán completarse correctamente. Esta respuesta informa del problema sin ocultar que MySQL es una dependencia obligatoria.

#### 18.1.2 SSOP-002: Almacenamiento de ficheros y recursos de aplicación

El subsistema SSOP-002 gestiona los artefactos que no son adecuados para almacenarse directamente como columnas relacionales. La aplicación utiliza `static/uploads` para las imágenes originales de diagnóstico, `static/results` para los mapas XAI y `training_results` para las configuraciones, logs y resultados del laboratorio. Los informes PDF se generan en las rutas que devuelven `pdf_generator.py` y `pdf_generator_mlops.py`. MySQL conserva las referencias a los ficheros cuando forman parte de una consulta o de un resultado.

La separación entre base de datos y sistema de ficheros evita insertar imágenes y documentos binarios grandes dentro de las tablas principales. La base de datos mantiene los metadatos que necesita el historial —modelo, etiqueta, confianza, usuario y rutas— y el sistema de ficheros conserva el contenido. Cuando SD-003 recupera una consulta, no recalcula ni copia el documento: utiliza las referencias persistidas para que la interfaz solicite el artefacto correspondiente.

Las plantillas Jinja2 y los recursos JavaScript pertenecen también a este subsistema de soporte, aunque se consumen desde la capa de presentación. `main.py` monta `static` como directorio de recursos y crea el directorio de resultados de entrenamiento si no existe. Las plantillas se resuelven mediante `Jinja2Templates` desde `templates`. Esta configuración permite que la aplicación sirva la interfaz sin un servidor frontend independiente ni un proceso de compilación adicional.

El almacenamiento se organiza según el origen del artefacto. Las cargas de diagnóstico reciben un nombre generado con una marca temporal y el nombre original; los resultados XAI se generan en un subdirectorio específico; y las sesiones de entrenamiento utilizan su identificador para agrupar configuración, logs y resultados. Esta organización facilita que el worker encuentre los artefactos a partir del payload y que el administrador pueda contabilizar sesiones inspeccionando sus configuraciones.

El control de acceso a los ficheros debe entenderse junto al control de acceso de los registros. La aplicación comprueba la propiedad de la consulta o de la sesión antes de devolver los metadatos que apuntan a los artefactos. Además, el entorno operativo debe limitar los permisos de escritura de los directorios al proceso de la aplicación y evitar la exposición directa de los directorios de datos cuando no sea necesaria. La implementación actual ofrece validación de tipo MIME y tamaño para las imágenes, pero no incorpora un antivirus ni un servicio independiente de análisis de contenido (Parlamento Europeo y Consejo de la Unión Europea, 2016; España, 2018).

La recuperación de este subsistema requiere copiar tanto los directorios de ficheros como las tablas que contienen sus rutas. Una copia de MySQL sin `static/uploads`, `static/results` o `training_results` restauraría referencias incompletas; una copia de los ficheros sin la base de datos perdería la asociación con usuarios, consultas y sesiones. Esta dependencia debe reflejarse en el procedimiento operativo de copia y restauración.

#### 18.1.3 SSOP-003: Entorno de ejecución e integraciones externas

SSOP-003 agrupa los elementos necesarios para iniciar la aplicación y comunicarse con los servicios que no forman parte del proceso local. El servidor se ejecuta con Uvicorn sobre Python 3.11 y utiliza FastAPI como framework web. El fichero `requirements.txt` fija las versiones de las dependencias principales, entre ellas TensorFlow, Keras, Transformers, `mysql-connector-python`, Groq, fpdf2, bcrypt, python-jose, slowapi, pytest y ruff.

El entorno virtual aísla estas dependencias de otras instalaciones de Python de la máquina. Antes de iniciar el sistema se debe comprobar que el intérprete activo corresponde al entorno del proyecto y que las versiones instaladas coinciden con el fichero de requisitos. Esta condición es especialmente importante para TensorFlow, Keras y Transformers, cuyas incompatibilidades pueden impedir la importación del motor de inferencia aunque el código de los routers sea correcto.

La aplicación se integra con Groq mediante `chatbot_service.py`. El servicio externo recibe los mensajes de configuración y devuelve una respuesta que el laboratorio procesa. El subsistema de soporte no expone una ruta genérica para llamar a Groq: la integración se encapsula en un único componente y utiliza `GROQ_API_KEY` desde el entorno. Esta frontera reduce la propagación de credenciales y permite sustituir o simular el proveedor durante las pruebas.

La carga de modelos Transformer constituye la otra integración externa relevante. `ml_engine.py` utiliza la configuración de Hugging Face para resolver las arquitecturas y pesos correspondientes. El primer uso puede requerir conectividad y espacio local para descargar o almacenar los modelos; los usos posteriores pueden beneficiarse de la caché disponible. La operación debe registrar como fallo de integración la imposibilidad de cargar un modelo, sin atribuir ese problema a la validación de la imagen o a la base de datos.

El entorno de publicación utiliza opcionalmente un túnel de Cloudflare para que un navegador externo acceda al servidor local. El túnel no aloja los datos ni ejecuta los modelos; solo proporciona el canal de entrada hasta Uvicorn. MySQL permanece en la máquina de ejecución y sus puertos no deben publicarse. Esta configuración conserva bajo control las versiones y los ficheros del proyecto, aunque no proporciona por sí misma alta disponibilidad ni escalado horizontal (IETF, 2018).

#### 18.1.4 SSOP-004: Calidad, pruebas y verificación operativa

El subsistema SSOP-004 agrupa las herramientas que permiten comprobar que los cambios no rompen el comportamiento existente. Las pruebas unitarias se encuentran en `tests/unit`, las de integración en `tests/integration` y las fixtures compartidas en `tests/conftest.py`. Los servicios externos se simulan mediante mocks y la base de datos se sustituye en las pruebas de integración por el entorno definido para ese nivel.

La estrategia de pruebas refleja la arquitectura. Los routers se prueban comprobando respuestas, autenticación, propiedad y errores; los servicios de aprendizaje automático se prueban con modelos simulados; el worker se prueba con trabajos controlados; y los middlewares se prueban de forma aislada para confirmar CSRF, cabeceras y limitación. La batería existente incluye pruebas de autenticación, validación de entradas, base de datos, inferencia, XAI, MLOps, cola, seguridad e internacionalización, además del flujo de autenticación integrado.

pytest-cov permite medir la cobertura de los módulos principales de `services`, `routers` y `database.py`. ruff verifica el estilo del código conforme a las convenciones de Python (van Rossum, Warsaw, & Coghlan, 2001) y el workflow de integración continua ejecuta las comprobaciones automatizadas. La calidad no se concentra en una única prueba de aceptación: se distribuye entre verificaciones rápidas durante el desarrollo y comprobaciones más amplias antes de integrar cambios.

Las fixtures deben mantenerse deterministas y sin datos reales de pacientes. Los modelos, clientes externos y conexiones de producción se sustituyen por dobles de prueba en los niveles que requieren aislamiento. La prueba de integración debe comprobar la colaboración entre capas, pero no convertir el entorno de producción ni la API de Groq en dependencias necesarias para cada ejecución local. Esta política mejora la repetibilidad y evita que una interrupción externa produzca falsos fallos del código.

### 18.2 Mecanismos de diseño transversales

Los mecanismos de diseño son reglas que se aplican a varios subsistemas independientemente de la funcionalidad concreta que implementen. Se distinguen de los subsistemas de soporte porque no son necesariamente un servicio con una identidad propia: son decisiones repetidas sobre cómo validar, autenticar, persistir, ejecutar y comunicar errores. En vitalXAI se identifican seis mecanismos principales.

#### 18.2.1 Configuración externa y separación de secretos

La configuración que cambia entre máquinas o que contiene información sensible se obtiene desde variables de entorno. Este mecanismo se aplica a autenticación, MySQL, Groq, duración de tokens y tamaño del pool. El código conserva valores por defecto únicamente para permitir el desarrollo local y emite advertencias cuando una configuración insegura puede afectar a la operación.

La separación de secretos evita que una clave JWT, una contraseña de MySQL o una clave de Groq quede incrustada en un router o en un servicio. Los componentes reciben la configuración en el momento de importación o de ejecución y utilizan nombres de variables comunes. El fichero de ejemplo o la guía de despliegue puede documentar los nombres requeridos, pero no debe contener valores válidos.

Este mecanismo también mejora la portabilidad. El mismo código puede ejecutarse con una base de datos local, una URL pública del túnel diferente o una duración de tokens ajustada al entorno sin modificar los routers. La configuración de desarrollo, pruebas y demostración debe mantenerse separada para evitar que una prueba utilice accidentalmente datos o credenciales del entorno operativo.

#### 18.2.2 Validación en las fronteras de entrada

Toda información procedente del navegador se considera no confiable hasta ser validada. FastAPI valida tipos y parámetros declarados por las rutas; los routers añaden comprobaciones de negocio; y los servicios vuelven a comprobar las condiciones necesarias antes de utilizar los datos en operaciones sensibles.

En el registro se comprueba el correo, la longitud de la contraseña y los campos obligatorios. En el diagnóstico se validan MIME y tamaño de la imagen. En el laboratorio se comprueba la existencia del dataset y la propiedad de la sesión. En la cola se valida la identidad y la pertenencia del trabajo. La validación del cliente mediante JavaScript puede mejorar la experiencia, pero no es la fuente de verdad: la petición debe poder rechazarse correctamente aunque se construya con un cliente distinto del frontend oficial.

Las consultas SQL utilizan parámetros separados de las instrucciones, y los nombres de archivo se generan dentro del servidor antes de copiar el contenido recibido. Los datos estructurados del payload de la cola se serializan como JSON y se interpretan según un tipo de trabajo controlado. La combinación de estas decisiones reduce el riesgo de que una entrada del usuario se convierta directamente en una consulta, una ruta o una orden ejecutable.

#### 18.2.3 Autenticación, autorización y propiedad de recursos

El mecanismo de identidad se reutiliza en todos los routers privados mediante `get_user_id_from_token()`. Esto evita que cada subsistema implemente una forma distinta de interpretar la sesión. Después de obtener el usuario, cada operación aplica el alcance correspondiente: propiedad del registro, rol administrativo o acceso general a una capacidad transversal.

La autorización se realiza cerca del recurso que se protege. El historial comprueba la propiedad de la consulta; el laboratorio comprueba la sesión; la cola comprueba el trabajo; y administración comprueba el rol. Esta decisión impide que un identificador enviado por el navegador sea suficiente para acceder a un objeto ajeno. Las funciones compartidas, como `_check_consultation_ownership()` y `_require_admin()`, concentran reglas repetidas sin convertirlas en un bypass general de seguridad.

CSRF, cabeceras y rate limiting se aplican mediante middleware o decoradores para que no dependan de que cada router recuerde incluirlos. No obstante, estos mecanismos son complementarios: un token CSRF válido no concede permisos sobre otro usuario y una cabecera de seguridad no sustituye a la comprobación de rol.

#### 18.2.4 Persistencia de estado y transacciones simples

La aplicación utiliza MySQL como fuente de verdad para el estado de cuentas, consultas, tokens y trabajos. Las operaciones de escritura siguen una secuencia corta: obtener conexión, preparar una consulta parametrizada, ejecutar, confirmar y cerrar. Esta política reduce el tiempo durante el que se mantiene un recurso del pool y facilita localizar la operación que produjo un error.

Los estados de los trabajos se persisten en lugar de mantenerse solo en una variable del proceso. Esto permite que el router de cola y el worker observen la misma información y que un reinicio pueda recuperar trabajos que quedaron en ejecución. La actualización condicional de `_claim_job()` actúa como mecanismo sencillo de exclusión para evitar que dos consumidores reclamen la misma tarea.

La persistencia de MySQL y la de ficheros deben coordinarse de manera explícita. Una fila de consulta puede existir antes de que todos sus artefactos hayan terminado de generarse, pero solo debe presentarse como resultado completado cuando el worker haya concluido el flujo. Los fallos de escritura de un informe o de un mapa XAI deben dejar constancia en el estado del trabajo y no ocultarse con una fila incompleta.

#### 18.2.5 Ejecución asíncrona y aislamiento de trabajos

La ejecución asíncrona se implementa mediante una cola persistida y un worker interno. Los routers registran el trabajo y devuelven la respuesta; `queue_worker.py` lo reclama y envía el cálculo pesado a `run_in_executor`. Este patrón libera el ciclo de petición y permite que la interfaz consulte el progreso sin esperar a que termine el entrenamiento o la inferencia.

El worker limita sus operaciones a los tipos explícitos `diagnosis`, `training` y `external_validation`. Cada tipo tiene una función de procesamiento que interpreta su payload, invoca al servicio adecuado y devuelve un resultado serializable. El bucle exterior captura los errores de un trabajo, los registra como `failed` y continúa con el siguiente. La recuperación de trabajos `running` al arrancar evita que una interrupción deje tareas invisibles.

La ejecución asíncrona no significa que todas las tareas tengan el mismo nivel de prioridad o el mismo mecanismo. Los entrenamientos y validaciones utilizan `job_queue`; el recálculo estadístico del laboratorio usa `BackgroundTasks`; y las peticiones de consulta permanecen síncronas porque solo recuperan información. Documentar esta diferencia evita que una futura modificación asuma garantías de persistencia para una tarea que actualmente se ejecuta como trabajo en segundo plano del proceso web.

#### 18.2.6 Errores, estados y comunicación con el usuario

Los errores se traducen en respuestas que la interfaz puede interpretar. Las rutas devuelven 401 cuando falta autenticación, 403 cuando el usuario no tiene autorización, 404 cuando el recurso no existe y 400 cuando los datos recibidos no cumplen una condición de negocio. Las excepciones inesperadas se convierten en respuestas 500 y, cuando pertenecen a un trabajo asíncrono, se conservan en el estado `failed` de la cola.

La capa de presentación recibe mensajes localizados mediante `lang.py`, por lo que los routers no deberían mezclar en cada respuesta textos técnicos sin una razón concreta. Al mismo tiempo, el cliente no debe recibir claves secretas, trazas completas ni credenciales. El detalle necesario para diagnosticar se conserva en la salida del servidor o en el estado de error del trabajo, mientras que la interfaz obtiene un mensaje comprensible y seguro.

Los estados `queued`, `running`, `completed`, `failed` y `cancelled` forman un contrato de comunicación entre el worker, los routers y el navegador. El usuario puede saber si la petición fue aceptada, si se está ejecutando, si terminó correctamente o si debe revisar un error. La uniformidad de este contrato reduce la necesidad de que cada vista invente una representación diferente para los trabajos.

#### 18.2.7 Modularidad, pruebas y evolución controlada

La modularidad se aplica separando routers, servicios, worker, persistencia y recursos de presentación. Los routers coordinan HTTP; los servicios encapsulan lógica especializada; `database.py` proporciona conexiones; `queue_worker.py` ejecuta trabajos; y las plantillas y scripts representan la interacción. La separación no es absoluta —los routers actuales acceden directamente a `get_db_connection()` en varias operaciones—, pero las responsabilidades principales siguen identificables y permiten probar cada grupo de forma aislada.

Las pruebas sirven como contrato evolutivo de esos límites. Los cambios en autenticación deben conservar las pruebas de tokens y cookies; los cambios en diagnóstico deben conservar la validación de imágenes y la integración con la cola; los cambios en MLOps deben conservar la propiedad de sesiones y los estados; y los cambios en middleware deben conservar las pruebas CSRF, cabeceras y rate limiting. Esta relación entre mecanismo de diseño y prueba reduce el riesgo de que una refactorización altere una garantía transversal sin que el cambio sea detectado.

#### 18.2.8 Ciclo de vida y sustitución controlada de componentes

Los componentes de soporte deben poder iniciarse, utilizarse y detenerse sin dejar recursos abiertos ni estados imposibles de interpretar. Durante el arranque, FastAPI carga la configuración, comprueba la base de datos e inicia el worker. Durante la operación, los routers solicitan conexiones y ficheros únicamente cuando los necesitan. Durante una parada o reinicio, los trabajos que estaban ejecutándose deben quedar identificados para que el siguiente arranque pueda devolverlos a la cola. Esta secuencia vincula el ciclo de vida del proceso web con la persistencia de `job_queue`.

La separación de soporte también facilita sustituir un componente si el entorno lo exige. MySQL podría cambiarse por otro motor compatible si se mantiene el contrato de `get_db_connection()` y se adaptan las consultas y el esquema; Groq podría reemplazarse si el servicio conversacional conserva la entrada de mensajes y la salida estructurada; y el directorio local de artefactos podría trasladarse a un almacenamiento especializado si se mantiene la relación entre rutas, usuarios y resultados. Estas posibilidades no forman parte de la implementación actual, pero muestran que la dependencia se concentra en puntos identificables y no se dispersa por toda la interfaz.

La sustitución no debe realizarse sin revisar los mecanismos transversales. Cambiar MySQL afecta al pool, a las transacciones, a las claves ajenas y a la recuperación de la cola; cambiar el almacenamiento afecta a las rutas de imágenes, informes y resultados; y cambiar el proveedor externo afecta a las credenciales, los tiempos de espera y el tratamiento de errores. Por ello, cualquier cambio de infraestructura debe acompañarse de pruebas de integración y de una comprobación de que los estados y permisos siguen siendo equivalentes.

El entorno de construcción conserva este principio mediante dependencias fijadas y pruebas reproducibles. Una nueva versión de TensorFlow, Keras, Transformers o `mysql-connector-python` no debe incorporarse únicamente porque resuelva un problema local: debe instalarse en un entorno aislado, ejecutarse la batería de pruebas y comprobarse que los modelos, los ficheros y las consultas mantienen el comportamiento esperado. La configuración de producción y la de pruebas deben permanecer separadas para que una migración o una prueba de recuperación no altere los datos de uso.

La arquitectura de soporte concluye así la estructura técnica de vitalXAI. SSOP-001 sostiene las relaciones y estados persistentes; SSOP-002 conserva los artefactos y recursos; SSOP-003 proporciona el entorno y las integraciones; SSOP-004 verifica el comportamiento. Sobre ellos se aplican la configuración externa, la validación, la seguridad, la persistencia de estados, la asincronía, la comunicación de errores y la modularidad. Ninguno de estos elementos sustituye a los subsistemas funcionales, pero todos son necesarios para que puedan ejecutarse de manera coherente con los requisitos y restricciones del proyecto.

La responsabilidad queda distribuida de forma verificable: el desarrollador mantiene el código y las pruebas; el operador prepara el entorno, las credenciales y MySQL; y el sistema conserva los estados y errores necesarios para diagnosticar una ejecución. Esta distribución evita que una incidencia de infraestructura se oculte como un fallo funcional y facilita localizar el punto de actuación adecuado.

Esta arquitectura deja definidos los puntos que deben comprobarse cuando se implanta o modifica la plataforma: disponibilidad de MySQL y de los directorios, validez de las variables de entorno, compatibilidad de las dependencias, funcionamiento del worker, conservación de los estados de la cola y ejecución de las pruebas automatizadas. La operación de vitalXAI depende de que estos elementos funcionen conjuntamente; por ello, el soporte no es un añadido posterior, sino la base que permite que la lógica clínica y experimental se ejecute de forma repetible y controlada.

El resultado es una infraestructura proporcionada al alcance académico y técnico del proyecto.

---

## Referencias del capítulo

Larman, C. (2004). *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3rd ed.). Prentice Hall.

Jacobson, I., Booch, G., & Rumbaugh, J. (1999). *The Unified Software Development Process*. Addison-Wesley.

IETF. (2018). *RFC 8446 – The Transport Layer Security (TLS) Protocol Version 1.3*. Obtenido de https://datatracker.ietf.org/doc/html/rfc8446

Parlamento Europeo y Consejo de la Unión Europea. (2016). Reglamento (UE) 2016/679 relativo a la protección de las personas físicas en lo que respecta al tratamiento de los datos personales y a la libre circulación de estos datos (RGPD). *Diario Oficial de la Unión Europea*, L119, 1-88.

España. (2018). Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales. *Boletín Oficial del Estado*, 294, 119788-119857.

van Rossum, G., Warsaw, B., & Coghlan, N. (2001). *PEP 8 – Style Guide for Python Code*. Obtenido de https://peps.python.org/pep-0008/
