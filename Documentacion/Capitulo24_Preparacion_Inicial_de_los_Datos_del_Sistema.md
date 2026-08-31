# Capítulo 24: Preparación inicial de los datos del sistema

Este capítulo fija las condiciones de datos necesarias para poner vitalXAI en funcionamiento por primera vez y describe cómo se mantiene el esquema cuando evoluciona. Después de definir el entorno y la construcción en el capítulo 23, aquí se concreta qué debe estar disponible, dónde se prepara y en qué orden se realizan las operaciones de inicialización (Elmasri & Navathe, 2016). El apartado completa el diseño de persistencia y sirve de referencia para las pruebas y la implantación.

El capítulo se organiza en dos apartados: el entorno de preparación de los datos, que describe el entorno tecnológico en el que se dispone la carga inicial, y los procedimientos de preparación y evolución del esquema, que definen el proceso, el orden de lanzamiento de los procedimientos y el diseño detallado de cada uno. El contenido se apoya en el modelo físico de datos del capítulo 19 y en la guía de despliegue del sistema, que fija los requisitos operativos de la puesta en marcha.

La carga inicial de vitalXAI no incluye datos semilla ni cuentas precargadas. El esquema relacional se crea y se comprueba automáticamente cuando arranca la aplicación, mientras que las cuentas se crean mediante el formulario de registro. Preparar el sistema consiste, por tanto, en disponer del esquema, de los datasets y pesos necesarios para la demostración y de la configuración que permite acceder a ellos. Los cambios futuros del esquema se gestionan manualmente y se registran en el registro de cambios de la base de datos, sin un proceso de migración formal.

## 24.1 Entorno de preparación de los datos

El entorno de preparación de los datos de vitalXAI reúne los elementos necesarios para la puesta en marcha del sistema. La preparación se realiza sobre el mismo equipo que ejecuta la aplicación: el entorno de desarrollo y de demostración del proyecto, que aloja el servidor, la base de datos, los conjuntos de imágenes y los pesos de los modelos. La tabla siguiente resume los elementos del entorno y su papel en la carga inicial.

| Elemento | Papel en la carga inicial |
|---|---|
| MySQL (MariaDB en XAMPP) | Almacén relacional donde la aplicación crea y verifica el esquema en el arranque. |
| Datasets de demostración | Conjuntos de imágenes de entrenamiento y de validación externa, necesarios para el diagnóstico y la experimentación. |
| Pesos de los modelos | Pesos de las arquitecturas entrenadas, necesarios para ejecutar la inferencia del diagnóstico. |
| Configuración del entorno | Variables de entorno con las credenciales y las rutas de los datos, suministradas mediante el archivo `.env`. |

La base de datos relacional se prepara mediante el servicio de MySQL del entorno, que en el desarrollo se ejecuta a través de XAMPP. La aplicación no requiere un script de instalación del esquema: la función `init_db()` de `database.py`, invocada en el arranque, ejecuta las sentencias `CREATE TABLE IF NOT EXISTS` que materializan el modelo físico de datos definido en el capítulo 19, creando las tablas `users`, `consultations`, `training_jobs`, `job_queue` y `refresh_tokens` cuando no existen (Oracle, 2024). La verificación de la conexión se realiza al iniciar la aplicación, que informa de la imposibilidad de conectar si el servicio no está activo.

Los datos de demostración comprenden los conjuntos de imágenes y los pesos de los modelos. El dataset de entrenamiento y evaluación XAI se conserva en `pneumoniacnn-main/Images`, y el conjunto independiente para la validación externa en `pneumoniacnn-main/ExternalDataset`; ambos se organizan en las subcarpetas `NORMAL/` y `PNEUMONIA/`. Los pesos de los modelos entrenados se conservan en `pneumoniacnn-main/results`, con los archivos correspondientes a cada arquitectura, y se cargan bajo demanda en la primera consulta de diagnóstico. La disponibilidad de estos artefactos es condición necesaria para el diagnóstico y para el laboratorio de experimentación.

La configuración del entorno se suministra mediante el archivo `.env`, que la aplicación carga en el arranque. La configuración incluye las credenciales de la base de datos (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_POOL_SIZE`), las claves de sesión (`JWT_SECRET_KEY` y los parámetros de expiración), la clave del asistente conversacional (`GROQ_API_KEY`) y las rutas de los datasets de demostración (`TFG_DEMO_DATASET` y `TFG_DEMO_EXTERNAL_DATASET`), que permiten lanzar los entrenamientos y la validación externa sin recurrir al selector de carpetas. Las cuentas de usuario no se precargan: se crean mediante el registro en la aplicación, de modo que la carga inicial de cuentas se realiza operativamente, conforme al flujo del subsistema de acceso.

El diagrama de despliegue de la figura 100 representa el entorno de preparación de los datos. La aplicación lee la configuración al arrancar, inicializa el esquema en la base de datos MySQL, carga los pesos de los modelos bajo demanda y accede a los datasets de demostración para la experimentación y la validación externa; el asistente conversacional se integra como proveedor externo.

```mermaid
flowchart LR
    subgraph SRV["Equipo de preparación (servidor)"]
        APP["Aplicación vitalXAI<br/>(Uvicorn / FastAPI)"]
        DB[(MySQL / MariaDB<br/>XAMPP)]
        DS["Datasets de demostración<br/>pneumoniacnn-main/Images<br/>+ ExternalDataset"]
        MD["Pesos de modelos<br/>pneumoniacnn-main/results"]
        CF["Configuración del entorno<br/>(.env)"]
    end
    subgraph EXT["Proveedores externos"]
        G["Groq (asistente IA)"]
    end
    APP -->|"inicializa el esquema"| DB
    APP -->|"carga pesos"| MD
    APP -->|"accede a los datasets"| DS
    APP -->|"lee la configuración"| CF
    APP -->|"API"| G
```

*Figura 100 - Diagrama de despliegue del entorno de preparación de los datos*

El diagrama refleja que la preparación inicial se resuelve en el equipo que aloja la aplicación, sin componentes de carga adicionales: la base de datos se inicializa desde la propia aplicación, y los datos de demostración y la configuración se disponen como artefactos del sistema de ficheros y variables de entorno. La verificación de los requisitos del entorno, incluidos el servicio de MySQL activo, la presencia de los datasets y de los pesos y la configuración correcta, constituye el punto de partida de los procedimientos de preparación descritos en el apartado siguiente.

## 24.2 Procedimientos de preparación y evolución del esquema

Los procedimientos de preparación de los datos definen el proceso por el que el sistema queda disponible para su primer uso, el orden o la jerarquía de lanzamiento de cada procedimiento y el diseño detallado de cada uno. El proceso se representa mediante el diagrama de actividad de la figura 101, que refleja la secuencia de preparación: la verificación de los requisitos del entorno, la inicialización del esquema, la disposición de los datos de demostración y de la configuración, y la creación de las cuentas de acceso.

```mermaid
flowchart TD
    INICIO["Inicio de la preparación"] --> REQ["Verificar requisitos del entorno<br/>(MySQL, datasets, pesos, configuración)"]
    REQ --> DEC{"¿Requisitos correctos?"}
    DEC -->|"No"| ERR["Corregir el requisito faltante"]
    ERR --> REQ
    DEC -->|"Sí"| MYSQL["Iniciar el servicio de MySQL (XAMPP)"]
    MYSQL --> CONF["Disponer de la configuración<br/>(datasets, pesos, .env)"]
    CONF --> ARR["Arrancar la aplicación (init_db)"]
    ARR --> ESQ["Crear y verificar el esquema<br/>(CREATE TABLE IF NOT EXISTS)"]
    ESQ --> REG["Crear las cuentas de acceso<br/>(registro de usuarios)"]
    REG --> FIN["Sistema preparado para el uso"]
```

*Figura 101 - Diagrama de actividad del proceso de preparación inicial de los datos*

El diagrama de actividad refleja el orden operativo de la preparación: primero se comprueban los requisitos y se inicia el servicio de la base de datos; después se dispone el archivo `.env` y los artefactos necesarios, y se arranca la aplicación, que crea y comprueba el esquema. Finalmente se crean las cuentas mediante el registro. La configuración debe estar disponible antes del arranque porque `main.py` la carga durante la importación de la aplicación.

El diseño detallado de cada procedimiento que participa en la preparación inicial se especifica en la tabla siguiente, con su orden de lanzamiento, su descripción y la verificación de su resultado.

| Procedimiento | Orden | Descripción | Verificación |
|---|---|---|---|
| Verificación de requisitos | 1 | Comprobar que el servicio de MySQL está disponible, que existen los datasets y los pesos de los modelos y que la configuración del entorno es correcta. | El entorno informa de los requisitos faltantes y permite corregirlos antes de continuar. |
| Inicialización del esquema | 2 | Ejecutar la aplicación, que invoca `init_db()` y crea las tablas del esquema con `CREATE TABLE IF NOT EXISTS` cuando no existen. | El arranque informa de la conexión a la base de datos y de la verificación de las tablas. |
| Configuración del entorno | 2 | Suministrar las variables de entorno del sistema mediante el archivo `.env`, con las credenciales, las claves y las rutas de los datasets. | La aplicación carga la configuración en el arranque y la utiliza en las operaciones de sesión, diagnóstico y experimentación. |
| Preparación de los datos de demostración | 3 | Disponer de los datasets de entrenamiento y de validación externa y de los pesos de los modelos en sus directorios correspondientes. | La solicitud de un diagnóstico carga los pesos del modelo; el laboratorio accede a las rutas de los datasets. |
| Creación de cuentas | 4 | Crear las cuentas de acceso mediante el registro de usuarios en la aplicación, sin datos de prueba precargados. | El nuevo usuario inicia sesión y accede al panel de diagnóstico. |

La configuración del entorno debe estar disponible antes de arrancar la aplicación, mientras que los datasets y los pesos deben estar presentes antes de utilizar las funciones que los necesitan. La creación de cuentas constituye un procedimiento operativo y continuo, que no forma parte de una carga única sino del funcionamiento normal del subsistema de acceso.

La evolución del esquema de la base de datos se gestiona de forma manual, sin un sistema de migraciones automáticas. Cuando el modelo físico de datos cambia, por la incorporación de una tabla, una columna o una restricción, la modificación se aplica actualizando las sentencias de creación de `database.py` y se registra en el registro de cambios de la base de datos del proyecto, con las sentencias SQL del cambio y las notas de reversión. `CREATE TABLE IF NOT EXISTS` solo evita el error cuando la tabla ya existe, pero no modifica su definición, por lo que no puede utilizarse como mecanismo de adaptación del esquema (Oracle, 2024). Esta decisión, coherente con la simplicidad del esquema y con el estado del proyecto, evita la complejidad de un sistema de migraciones mientras la base de datos se encuentra en una fase estable; si el esquema evolucionara hacia cambios destructivos o una base de datos con datos persistidos críticos, la incorporación de un mecanismo de migraciones formal debería evaluarse conforme al registro de decisiones del proyecto.
