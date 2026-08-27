# Capítulo 11: Definición del ámbito del sistema

El contexto y el estado del arte en el que se inscribe vitalXAI se presentaron en el capítulo 1, donde se describieron el problema de la neumonía, la radiografía de tórax como imagen digital, la evolución del aprendizaje profundo aplicado al diagnóstico por imagen, los conjuntos de datos y los modelos de referencia, y las plataformas MLOps existentes. Este capítulo no repite ese análisis: asume lo allí expuesto y se centra en delimitar el ámbito del sistema, es decir, qué capacidades incluye vitalXAI como producto, bajo qué entorno tecnológico, con qué normativa y para qué usuarios.

vitalXAI pretende ocupar el espacio que los sistemas existentes no cubren de forma conjunta: una plataforma web que reúna el diagnóstico asistido con inteligencia artificial explicable, un laboratorio de entrenamiento reproducible accesible sin escribir código y una validación estadística rigurosa de los resultados. El sistema combina la potencia de los modelos de investigación, la capacidad de gestión de las plataformas MLOps y la sencillez de uso de los productos comerciales, con la transparencia que estos últimos no ofrecen.

La elección de una plataforma web es deliberada. Para el usuario final, la plataforma elimina cualquier requisito de instalación: el acceso se realiza desde un navegador, sin dependencia de un sistema operativo concreto ni de un equipo determinado, lo que descarta los desarrollos móviles o de escritorio, que exigirían instalar y mantener una aplicación en cada terminal. Conviene precisar, no obstante, que esa ausencia de requisitos técnicos se refiere al cliente y no al sistema en su conjunto. La operación de vitalXAI impone exigencias propias de infraestructura: el entrenamiento requiere una estación de trabajo con GPU NVIDIA compatible con CUDA, la publicación del servicio depende de un túnel de Cloudflare y ciertas operaciones del laboratorio, como la selección de la carpeta del dataset (RF-019), se realizan sobre el sistema de ficheros del servidor. Estos requisitos, que se detallan en la sección 11.1, recaen sobre el entorno que despliega y mantiene la plataforma, mientras que el profesional que la utiliza solo necesita un navegador.

Esta decisión condiciona de forma notable el alcance del sistema y la arquitectura que debe adoptarse, porque toda la complejidad computacional —los modelos, el entrenamiento, el almacenamiento de los datos— queda confinada en el servidor. La plataforma se estructura, así, en dos caras complementarias: la que ve el usuario, pensada para ser lo más simple posible, y la que no ve, donde residen los motores de cálculo.

Desde el punto de vista funcional, el sistema se organiza en torno a dos núcleos principales y a varias capacidades de apoyo, y conviene anticiparlos aquí porque constituyen el esqueleto sobre el que se definen los objetivos y los requisitos. El primer núcleo es la interfaz clínica de diagnóstico: permite al facultativo cargar una radiografía, seleccionar la arquitectura con la que desea realizar la consulta, obtener un diagnóstico con su nivel de confianza, visualizar los mapas de explicabilidad que justifican la predicción y descargar un informe en PDF, manteniendo además un historial de consultas aislado por usuario que el profesional puede consultar, renombrar o depurar cuando lo necesite. El segundo núcleo es el laboratorio MLOps: permite al investigador configurar y lanzar experimentos de entrenamiento mediante un asistente conversacional, monitorizar su progreso en tiempo real y consultar los resultados comparativos y estadísticos, incluyendo el ranking de modelos, las matrices de significación y los análisis de explicabilidad y calibración.

Junto a estos dos núcleos, el sistema incorpora una serie de capacidades de apoyo que lo hacen operativo en condiciones reales de uso. La ejecución asíncrona de las tareas largas garantiza que la interfaz no se bloquee durante los entrenamientos, que pueden prolongarse durante horas. El soporte multilingüe amplía la accesibilidad de la plataforma a usuarios de distintas procedencias. El panel de administración permite a un usuario con rol de administrador gestionar las cuentas y supervisar la actividad del sistema. Y la capa de autenticación y seguridad protege los datos de cada usuario de forma transversal. Para formalizar este alcance, en primer lugar se definen los objetivos del sistema; a continuación se caracterizan el entorno tecnológico, la normativa aplicable y los perfiles de usuario que interactuarán con la plataforma.

## Objetivos del sistema

Los objetivos del sistema constituyen la declaración formal de lo que vitalXAI debe conseguir como producto. Se obtienen a partir de las reuniones mantenidas con el tutor y de los objetivos generales del proyecto, y sirven de anclaje para los requisitos que se definen en los capítulos siguientes del análisis. Cada objetivo se describe mediante una ficha en la que se recogen su identificador, su nombre, la descripción de lo que debe lograr el sistema, su importancia dentro del conjunto y el estado de la decisión. Conviene distinguir estos objetivos de los objetivos del plan de proyecto presentados en la primera parte de la memoria: aquellos describen lo que el alumno debe conseguir durante el desarrollo; estos describen lo que el sistema debe ofrecer como producto final, con independencia de cómo se implemente. Para que el lector pueda comprobar que el producto especificado cubre los compromisos adquiridos en el plan de proyecto, la tabla 15, presentada al final de esta sección, establece la correspondencia entre cada objetivo del sistema y los objetivos específicos del plan que lo sustentan.

**OBJ-001 – Diagnóstico asistido con inteligencia artificial explicable.**

El diagnóstico asistido es el núcleo de la plataforma y el punto de partida de todo el sistema. Un profesional sanitario, sin conocimientos de inteligencia artificial, debe poder cargar una radiografía de tórax y obtener, en un tiempo razonable, un diagnóstico con su nivel de confianza y una explicación visual de los motivos que sustentan la decisión del modelo. La confianza es importante porque permite al facultativo calibrar la fiabilidad de la predicción, y la explicación visual es importante porque le permite comprobar si el modelo se está fijando en las regiones pulmonares correctas. Esta ficha fija ese compromiso.

| Campo | Contenido |
|---|---|
| ID | OBJ-001 |
| Nombre | Diagnóstico asistido con inteligencia artificial explicable |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe permitir al profesional sanitario cargar una radiografía de tórax, seleccionar una arquitectura de deep learning y obtener un diagnóstico con su nivel de confianza, acompañado de los mapas de explicabilidad que justifican la predicción. |
| Importancia | Alta |
| Estado | Aprobado |
| Comentarios | Este objetivo recoge el núcleo clínico del sistema. El mecanismo concreto de generación de las explicaciones corresponde al ámbito del diseño. |

*Tabla 4 - OBJ-001: Diagnóstico asistido con inteligencia artificial explicable*

**OBJ-002 – Gestión del historial de consultas.**

Un facultativo realiza numerosas consultas a lo largo del tiempo, y cada una de ellas debe quedar registrada para poder ser consultada, revisada o corregida posteriormente. Sin un historial organizado, el profesional perdería la capacidad de comparar la evolución de un mismo caso o de recuperar un diagnóstico anterior. Este objetivo garantiza que el sistema conserve el historial completo de diagnósticos de cada usuario de forma aislada y gestionable.

| Campo | Contenido |
|---|---|
| ID | OBJ-002 |
| Nombre | Gestión del historial de consultas |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe conservar el historial de consultas de diagnóstico de cada usuario, permitiendo consultarlas, renombrarlas y eliminarlas, de modo que cada profesional gestione únicamente sus propios registros. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | Este objetivo complementa al OBJ-001 y refuerza el aislamiento de datos entre usuarios. |

*Tabla 5 - OBJ-002: Gestión del historial de consultas*

**OBJ-003 – Generación de informes descargables.**

Los resultados de un diagnóstico no deben quedarse en la pantalla: el profesional necesita un documento que pueda archivar, imprimir o incorporar a su flujo de trabajo habitual. Este objetivo cubre la generación de informes en formato PDF. El informe consolidado de una sesión de entrenamiento está formalizado en el requisito RF-030, que fija su contenido (configuración del experimento, ranking de modelos, comparativas estadísticas, validación externa y métricas de explicabilidad y calibración). El informe individual de un diagnóstico se entrega junto con el resultado de la consulta: la capacidad está implementada y verificada en la prueba PU-017, aunque la especificación de requisitos no le dedica un requisito funcional propio, una laguna que deberá resolverse en una revisión posterior del catálogo de requisitos.

| Campo | Contenido |
|---|---|
| ID | OBJ-003 |
| Nombre | Generación de informes descargables |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe generar informes en formato PDF. El informe consolidado de cada sesión de entrenamiento se especifica en el requisito RF-030. El informe individual de cada diagnóstico se genera junto con el resultado de la consulta y se verifica en la prueba PU-017. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | El informe de sesión está formalizado en el requisito RF-030. El informe individual del diagnóstico está implementado y probado (PU-017), pero no dispone de un requisito funcional propio en la especificación actual, laguna que debe corregirse en una revisión posterior. |

*Tabla 6 - OBJ-003: Generación de informes descargables*

**OBJ-004 – Laboratorio de entrenamiento MLOps.**

El segundo núcleo del sistema es el laboratorio de entrenamiento. Su propósito es que un investigador pueda configurar y lanzar experimentos de entrenamiento de modelos sin escribir código, apoyándose en un asistente conversacional que interpreta sus indicaciones y las traduce a la configuración técnica del pipeline. El usuario debe poder consultar los resultados de forma organizada y conocer el estado de sus trabajos. Conviene distinguir aquí dos nociones relacionadas pero distintas: el estado de la cola de trabajos, cubierto por el requisito RF-036 (pendiente, en ejecución, completado o fallido), y el progreso del entrenamiento por épocas, que el laboratorio calcula y muestra mientras la ejecución avanza. El cálculo de ese progreso está implementado y verificado en la prueba PU-023, aunque la especificación de requisitos no le dedica un requisito funcional propio, laguna que deberá resolverse en una revisión posterior del catálogo de requisitos.

| Campo | Contenido |
|---|---|
| ID | OBJ-004 |
| Nombre | Laboratorio de entrenamiento MLOps |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe permitir al usuario configurar y lanzar experimentos de entrenamiento de modelos mediante un asistente conversacional, consultar los resultados generados por el pipeline de forma organizada y conocer el estado de sus trabajos. |
| Importancia | Alta |
| Estado | Aprobado |
| Comentarios | Este objetivo engloba el ciclo completo del experimento desde la perspectiva del usuario: configurar, lanzar, consultar el estado y recuperar los resultados. El estado de la cola está cubierto por el requisito RF-036; el progreso por épocas está implementado y verificado en la prueba PU-023, pero carece de un requisito funcional propio en la especificación actual. |

*Tabla 7 - OBJ-004: Laboratorio de entrenamiento MLOps*

**OBJ-005 – Evaluación rigurosa de los modelos.**

De nada sirve entrenar modelos si no se puede determinar de forma objetiva cuál es mejor y si las diferencias observadas entre ellos son reales o fruto del azar. Este objetivo garantiza que el sistema automatice la evaluación estadística de los modelos —comparación de rendimiento, validación externa sobre una cohorte independiente y contrastes de significación— y que presente los resultados de forma comprensible para el investigador, de manera que las conclusiones puedan defenderse con rigor científico.

| Campo | Contenido |
|---|---|
| ID | OBJ-005 |
| Nombre | Evaluación rigurosa de los modelos |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe automatizar la evaluación estadística de los modelos entrenados: comparación de rendimiento, validación externa sobre una cohorte independiente y contrastes de significación, presentando los resultados de forma comprensible para el usuario. |
| Importancia | Alta |
| Estado | Aprobado |
| Comentarios | La concreción de las pruebas estadísticas se especifica en los requisitos derivados de este objetivo. |

*Tabla 8 - OBJ-005: Evaluación rigurosa de los modelos*

**OBJ-006 – Reproducibilidad de los experimentos.**

La reproducibilidad es una exigencia de la investigación científica y, en particular, del aprendizaje automático, donde una inicialización aleatoria distinta o un orden de datos diferente pueden alterar los resultados. Este objetivo garantiza que cada experimento quede asociado a su configuración completa y a las semillas aleatorias utilizadas, de modo que cualquier resultado pueda verificarse y replicarse bajo las mismas condiciones.

| Campo | Contenido |
|---|---|
| ID | OBJ-006 |
| Nombre | Reproducibilidad de los experimentos |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe favorecer la reproducibilidad de los experimentos de entrenamiento, fijando las semillas aleatorias y almacenando la configuración completa de cada sesión junto con sus resultados, de modo que los resultados puedan verificarse y replicarse bajo las mismas condiciones. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | Este objetivo responde a las carencias de reproducibilidad identificadas en la literatura sobre aprendizaje automático. |

*Tabla 9 - OBJ-006: Reproducibilidad de los experimentos*

**OBJ-007 – Acceso seguro y personalizado al sistema.**

El sistema trata información de carácter clínico, aunque anonimizada, y cada usuario debe disponer de un espacio de trabajo aislado. Este objetivo cubre el registro de nuevos usuarios, la autenticación, el cierre de sesión y la garantía de que cada profesional accede únicamente a sus propios datos. El mecanismo de autorización que aquí se define distingue los perfiles de acceso, pero las operaciones de gobierno reservadas al administrador se recogen como capacidad propia en el OBJ-011, de modo que ambos objetivos no se solapan: el acceso seguro determina quién puede entrar y sobre qué datos, y la administración cubre las operaciones sobre el conjunto de la plataforma.

| Campo | Contenido |
|---|---|
| ID | OBJ-007 |
| Nombre | Acceso seguro y personalizado al sistema |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe disponer de un módulo de gestión de usuarios que permita el registro, la autenticación y el cierre de sesión de forma segura, garantizando que cada usuario opere únicamente sobre sus propios datos y consultas. El rol de administrador y las operaciones de gobierno se recogen en el OBJ-011. |
| Importancia | Alta |
| Estado | Aprobado |
| Comentarios | La autenticación es un requisito no negociable dado el carácter clínico de los datos gestionados. El mecanismo concreto de autenticación corresponde al diseño. |

*Tabla 10 - OBJ-007: Acceso seguro y personalizado al sistema*

**OBJ-008 – Persistencia y trazabilidad de la información.**

El sistema debe almacenar de forma persistente las consultas de diagnóstico y las sesiones de entrenamiento, junto con su configuración y sus resultados, de modo que el usuario pueda consultar su historial en cualquier momento. La persistencia no es una funcionalidad visible para el usuario final, sino la base sobre la que se sustentan el historial clínico, la comparación de experimentos y la trazabilidad de los resultados.

| Campo | Contenido |
|---|---|
| ID | OBJ-008 |
| Nombre | Persistencia y trazabilidad de la información |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe almacenar de forma persistente las consultas de diagnóstico y las sesiones de entrenamiento, junto con su configuración y sus resultados, de modo que el usuario pueda consultar su historial en cualquier momento. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | La persistencia es un requisito transversal: sustenta al resto de los objetivos aunque no sea una funcionalidad visible para el usuario final. |

*Tabla 11 - OBJ-008: Persistencia y trazabilidad de la información*

**OBJ-009 – Usabilidad e internacionalización de la interfaz.**

El sistema está pensado para usuarios sin formación técnica, por lo que la interfaz debe ser intuitiva y no exigir en ningún momento interactuar con código ni con entornos de programación. Además, el sistema debe estar disponible en varios idiomas, de modo que el usuario pueda cambiar de idioma de forma dinámica, ampliando la accesibilidad de la plataforma a entornos multilingües.

| Campo | Contenido |
|---|---|
| ID | OBJ-009 |
| Nombre | Usabilidad e internacionalización de la interfaz |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe ofrecer una interfaz web intuitiva para usuarios con perfil no técnico, que permita realizar todas las operaciones sin interactuar con código ni con entornos de programación, y debe estar disponible en varios idiomas, permitiendo cambiar de idioma de forma dinámica. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | La usabilidad determina la adopción del sistema por parte de los usuarios finales; no afecta a la corrección funcional de los modelos. |

*Tabla 12 - OBJ-009: Usabilidad e internacionalización de la interfaz*

**OBJ-010 – Ejecución asíncrona de tareas de larga duración.**

El entrenamiento de un modelo de deep learning puede prolongarse durante horas, y durante ese tiempo la plataforma debe seguir respondiendo al usuario. Este objetivo garantiza que las tareas largas —entrenamientos, análisis de explicabilidad y validación externa— se ejecuten de forma asíncrona a través de una cola de trabajos, de modo que la interfaz permanezca operativa y el usuario pueda consultar el estado de cada tarea e incluso cancelar las tareas pendientes.

| Campo | Contenido |
|---|---|
| ID | OBJ-010 |
| Nombre | Ejecución asíncrona de tareas de larga duración |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe ejecutar las tareas de larga duración —entrenamientos, análisis de explicabilidad y validación externa— de forma asíncrona, de modo que la interfaz permanezca operativa durante su ejecución y el usuario pueda consultar el estado de cada tarea. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | Este objetivo garantiza la disponibilidad de la plataforma durante los procesos computacionales más costosos. |

*Tabla 13 - OBJ-010: Ejecución asíncrona de tareas de larga duración*

**OBJ-011 – Administración de la plataforma.**

El gobierno de una plataforma con múltiples usuarios requiere de un perfil con privilegios de administración que pueda gestionar las cuentas y supervisar la actividad registrada. Este objetivo cubre la existencia de un panel de administración y de un rol diferenciado dentro del mecanismo de autorización. La frontera con el OBJ-007 queda así definida: el acceso seguro garantiza quién puede entrar y sobre qué datos, mientras que la administración cubre las operaciones de gobierno sobre el conjunto de la plataforma, reservadas al administrador. Esta frontera se refleja en la trazabilidad de los requisitos: el requisito transversal de roles y control de acceso (RF-006) se asocia a ambos objetivos, mientras que la auditoría de la actividad administrativa (RNF-006) se asocia únicamente al OBJ-011.

| Campo | Contenido |
|---|---|
| ID | OBJ-011 |
| Nombre | Administración de la plataforma |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe disponer de un panel de administración que permita gestionar las cuentas de usuario y supervisar las consultas y sesiones de entrenamiento registradas en la plataforma, con acceso restringido al rol de administrador. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | Este objetivo define la administración como las operaciones de gobierno reservadas al administrador, complementando al OBJ-007, que cubre el acceso seguro y el aislamiento de datos. La auditoría de la actividad administrativa se especifica en el requisito no funcional RNF-006. |

*Tabla 14 - OBJ-011: Administración de la plataforma*

La tabla 15 establece la correspondencia entre los once objetivos del sistema y los objetivos específicos del plan de proyecto presentados en el capítulo 2 (OE1 a OE11). No se trata de una relación uno a uno: varios objetivos del sistema se apoyan en un mismo objetivo del plan, y algunos objetivos del plan son de carácter científico-metodológico y sustentan a más de un objetivo del producto. El objetivo específico OE1 (revisar el estado del arte) no figura en la correspondencia porque pertenece a la fase de fundamentación del proyecto y no se materializa como una capacidad del producto.

| Objetivo del sistema | Objetivo(s) específico(s) del plan | Relación |
|---|---|---|
| OBJ-001 Diagnóstico asistido con IA explicable | OE5, OE8 | La explicabilidad (OE5) y la interfaz clínica (OE8) sustentan el diagnóstico explicable. |
| OBJ-002 Gestión del historial de consultas | OE2 | La arquitectura de persistencia (OE2) soporta el historial. |
| OBJ-003 Generación de informes descargables | OE8, OE9 | El informe individual se entrega con el diagnóstico (OE8); el informe de sesión se consolida en el laboratorio (OE9). |
| OBJ-004 Laboratorio de entrenamiento MLOps | OE9 | El laboratorio y el asistente conversacional (OE9) materializan el laboratorio. |
| OBJ-005 Evaluación rigurosa de los modelos | OE4, OE6 | El pipeline (OE4) produce las métricas; la validación externa y el análisis estadístico (OE6) las evalúan. |
| OBJ-006 Reproducibilidad de los experimentos | OE7 | La reproducibilidad y la trazabilidad (OE7) se materializan en este objetivo. |
| OBJ-007 Acceso seguro y personalizado | OE3 | El control de acceso (OE3) sustenta este objetivo. |
| OBJ-008 Persistencia y trazabilidad | OE2 | La arquitectura de persistencia (OE2) sustenta este objetivo. |
| OBJ-009 Usabilidad e internacionalización | OE8, OE11 | La usabilidad se garantiza en la interfaz (OE8); la internacionalización (OE11). |
| OBJ-010 Ejecución asíncrona de tareas | OE10 | El procesamiento asíncrono (OE10) se materializa en este objetivo. |
| OBJ-011 Administración de la plataforma | — | Sin objetivo específico directo: la administración amplía el alcance planificado y se apoya, para el rol, en el control de acceso (OE3). |

*Tabla 15 - Correspondencia entre los objetivos del sistema y los objetivos específicos del plan de proyecto*

## 11.1 Contexto tecnológico y restricciones de entorno
El sistema no se construye sobre un lienzo en blanco, sino que se incorpora a un ecosistema tecnológico preexistente que establece condiciones para su desarrollo. Comprender este contexto es fundamental durante el análisis, porque delimita el marco en el que el sistema debe operar. Este apartado distingue con claridad dos tipos de elementos: las restricciones que el entorno impone de forma ineludible y que condicionan cualquier diseño, y las decisiones tecnológicas que corresponden al proyecto y que, por tanto, se justifican en la parte de diseño de la memoria.

La principal imposición del entorno es el lenguaje de programación. El ecosistema de aprendizaje automático en el que se apoya el proyecto —las librerías de deep learning, los formatos de los modelos y las herramientas de evaluación— está desarrollado íntegramente en Python, por lo que el entorno de ejecución del sistema debe ser compatible con Python y con las librerías de ese ecosistema. Esta restricción es ineludible: optar por otro lenguaje supondría renunciar a la práctica totalidad del ecosistema científico, de las arquitecturas preentrenadas y de los procedimientos experimentales sobre los que se sustenta el proyecto.

La segunda imposición del entorno es la necesidad de computación GPU para el entrenamiento. Una red neuronal está formada por millones de parámetros que se ajustan durante el entrenamiento, y en cada paso del proceso hay que ejecutar un número ingente de operaciones matemáticas sobre los píxeles de las imágenes. Un procesador convencional (CPU) ejecuta estas operaciones de forma secuencial, lo que convertiría el entrenamiento de los modelos en un proceso inviable en los plazos de un Trabajo Fin de Grado. Las unidades de procesamiento gráfico (GPU) ejecutan miles de operaciones en paralelo, lo que reduce drásticamente los tiempos de entrenamiento. El proyecto se desarrolla sobre un equipo portátil equipado con una GPU NVIDIA RTX 4060 Laptop con 8 GB de VRAM, capacidad suficiente para entrenar, con tamaños de lote reducidos y precisión mixta, las arquitecturas más exigentes del banco de pruebas (ViT-384 y EfficientNetB7). Sin esa capacidad, la fase de validación cruzada de los modelos —en la que cada arquitectura se entrena varias veces— resultaría inviable.

El equipo forma parte de la infraestructura ya disponible para el desarrollo del proyecto: el plan de proyecto lo refleja así y no imputa su amortización al coste del TFG. La alternativa de contratar instancias de computación en la nube fue descartada por dos motivos. El primero es económico: alojar el entrenamiento en la nube supone un coste por hora de uso que, multiplicado por las decenas de entrenamientos que exige el proyecto, se convierte en una partida significativa. El segundo es práctico: trabajar en local permite disponer de los pesos de los modelos y de los datos de forma inmediata, sin depender de la conectividad ni de las políticas de almacenamiento de un proveedor externo. Esta restricción tiene una consecuencia directa sobre la planificación: los tiempos de entrenamiento deben estimarse con prudencia y los experimentos más costosos deben programarse con antelación.

Sobre estas imposiciones, el sistema opera en un marco tecnológico que conviene fijar a efectos de análisis. El proyecto se apoya en un servicio web que atiende las peticiones del navegador, un motor de aprendizaje automático para las arquitecturas convolucionales y de atención, una base de datos relacional para la persistencia y un asistente conversacional integrado con un gran modelo de lenguaje. La elección concreta de cada uno de estos componentes —el framework de servicios web, el gestor de base de datos, las librerías y sus versiones— es una decisión de diseño y, como tal, se selecciona y justifica en la parte de diseño de la memoria. El análisis únicamente necesita conocer el contexto tecnológico de trabajo, que se resume en la tabla 16, sin entrar en decisiones de implementación como el algoritmo de cifrado de contraseñas, la librería de gestión de tokens o el limitador de peticiones, que pertenecen al diseño.

| Componente | Tecnología |
|---|---|
| Lenguaje | Python |
| Servicio web y presentación | FastAPI y Uvicorn, con renderizado de plantillas Jinja2 |
| Persistencia | MySQL |
| Aprendizaje automático | TensorFlow y Keras (arquitecturas convolucionales) |
| Modelos de atención | Ecosistema Hugging Face Transformers |
| Visión por computador | OpenCV |
| Análisis de datos | pandas, NumPy, scikit-learn, SciPy |
| Representación gráfica | matplotlib, seaborn |
| Informes PDF | fpdf2 |
| Asistente conversacional | API de Groq (modelo de lenguaje) |

*Tabla 16 - Contexto tecnológico del sistema*

La tabla anterior recoge el marco tecnológico de trabajo, no la especificación de implementación. Las versiones exactas de las dependencias, las librerías de seguridad (cifrado de contraseñas, gestión de tokens, limitación de peticiones) y las herramientas de calidad y pruebas se seleccionan y justifican en la parte de diseño, donde se describe el entorno de construcción del sistema.

En cuanto al despliegue, la forma de publicar el servicio es también una decisión del proyecto, no una imposición del entorno. El sistema se ejecuta sobre la máquina local de desarrollo y debe ser accesible desde cualquier navegador, incluidos los de equipos ajenos. Existen varias alternativas para lograr ese acceso: abrir puertos en el router del entorno local, alojar el servicio en una máquina virtual con dirección pública o desplegarlo en un contenedor en la nube. Para este proyecto se opta por un túnel seguro: un canal cifrado que conecta el servidor local con un dominio público proporcionado por un proveedor, de modo que quien accede a ese dominio llega, a través del canal cifrado, al servidor local. Se utiliza un túnel de Cloudflare porque evita exponer el equipo a los riesgos de abrir puertos en el router y no requiere alquilar infraestructura adicional; las alternativas (apertura de puertos, VPS o contenedor en la nube) se descartan por razones de seguridad, coste y simplicidad operativa. La justificación detallada de esta elección se desarrolla en la parte de diseño, junto con el resto de decisiones de despliegue.

En cuanto a la reproducibilidad, la fijación de versiones y el aislamiento del entorno son condiciones necesarias, pero no suficientes, para reproducir un experimento: garantizan que dos ejecuciones parten del mismo entorno de software, lo que elimina una fuente importante de variabilidad. No obstante, como se señala en el objetivo de reproducibilidad (OBJ-006), la ejecución de los modelos no pretende un determinismo bit a bit entre ejecuciones, sino que cualquier resultado pueda verificarse y replicarse bajo las mismas condiciones. La gestión de las dependencias se orienta, por tanto, a que el entorno sea coherente y reconstruible, no a eliminar toda variabilidad numérica del proceso de entrenamiento.

En definitiva, la distinción entre restricciones y decisiones permite evaluar el sistema sabiendo qué elementos venían condicionados de antemano y cuáles eran libres. La elección de Python y la necesidad de computación GPU son imposiciones del entorno, ineludibles para el proyecto. En cambio, el framework de servicios web, la base de datos, las librerías de seguridad, las versiones concretas de las dependencias y el mecanismo de despliegue son decisiones de diseño que se justifican en la parte de diseño de la memoria y que no deben atribuirse al entorno.

## 11.2 Normativa y estándares de referencia

El desarrollo del sistema está sujeto a una serie de normas y estándares que se derivan de su propia naturaleza y del ámbito en el que se inscribe. Estas normas condicionan desde la estructura del proyecto hasta el tratamiento de los datos personales, el ámbito sanitario, la seguridad de las comunicaciones y la calidad del código. Conviene examinarlas una a una porque cada una afecta a un aspecto distinto del sistema.

En primer lugar, la cuestión más sensible es la de la protección de datos. El sistema gestiona cuentas de usuarios registrados y procesa imágenes de origen médico. Los datos personales son, por definición, cualquier información relativa a una persona física identificada o identificable, y en el ámbito sanitario esa sensibilidad se multiplica: una imagen de un paciente, su historial de consultas o los resultados asociados a su cuenta son información que debe tratarse con las máximas garantías. En el ámbito de la Unión Europea se aplica el Reglamento General de Protección de Datos (RGPD, Reglamento UE 2016/679), que regula el tratamiento de los datos personales y establece principios como la minimización de los datos —no recoger más información de la necesaria—, la limitación de la finalidad —no usar los datos para fines distintos de los que motivaron su recogida— y la garantía del anonimato cuando se manejan datos de naturaleza biomédica (Parlamento Europeo y Consejo de la Unión Europea, 2016). A nivel nacional, el RGPD se complementa con la Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales, que adapta el reglamento europeo al ordenamiento jurídico español (España, 2018). Conviene señalar que el acceso del administrador a los datos de otros usuarios en el ejercicio de sus funciones de supervisión constituye igualmente un tratamiento de datos: queda acotado al rol y a la finalidad de gobierno de la plataforma, se recoge como excepción del aislamiento de datos en el requisito RF-005 y se regula en el módulo de administración (RF-033 a RF-035).

Conviene ser preciso sobre la anonimización. El proyecto asume que las imágenes que llegan al sistema están anonimizadas y que los conjuntos de datos utilizados son públicos y anónimos, pero esa asunción no equivale a una garantía implementada: si un facultativo sube una radiografía con identificadores visibles en la imagen o con metadatos DICOM que revelen la identidad del paciente, el sistema los almacena junto con la imagen. En el estado actual del proyecto no existe un mecanismo que despoje automáticamente esos metadatos ni una validación que compruebe la ausencia de identificadores antes de aceptar una carga. Esta circunstancia debe documentarse como una limitación: la anonimización previa recae hoy en el responsable de la captura, y una evolución del sistema debería incorporar la limpieza de metadatos y la detección de identificadores como requisitos explícitos.

El tratamiento por parte de terceros merece también atención. El asistente conversacional del laboratorio envía los mensajes del usuario a la API de Groq, un proveedor externo, para obtener las respuestas que se traducen en la configuración del experimento. Aunque el contenido de esas conversaciones se refiere a la configuración de entrenamientos y no a datos clínicos de pacientes, constituye un envío de información del usuario a un tercero y debe hacerse constar como tal. El proyecto lo limita en la medida de lo posible: la conversación se orienta a parámetros técnicos del experimento, no se ofrecen campos para introducir datos personales y el tratamiento se ampara en la necesidad de prestar el servicio al propio usuario. No obstante, esta sección debe dejar constancia de la transferencia para que el responsable del sistema pueda valorar, en cada despliegue, si debe formalizarse un encargo de tratamiento o una cláusula de protección de datos con el proveedor.

En segundo lugar, el sistema se inscribe en el ámbito de las tecnologías sanitarias y de la inteligencia artificial, donde dos reglamentos europeos son especialmente relevantes. El Reglamento (UE) 2017/745 sobre productos sanitarios (MDR) establece los requisitos que debe cumplir un producto destinado a un fin médico para su comercialización en la Unión Europea; un sistema de ayuda al diagnóstico, según su finalidad declarada, podría quedar comprendido en su ámbito, aunque el proyecto se desarrolla en un contexto académico y de investigación, sin intención de comercialización. Por otra parte, el Reglamento (UE) 2024/1689 por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de IA) clasifica los sistemas de IA según su riesgo y establece obligaciones específicas para los de alto riesgo; un sistema de IA destinado a la asistencia al diagnóstico médico es, con alta probabilidad, un sistema de alto riesgo bajo esa norma, con independencia de que el proyecto actual se limite a un entorno de demostración. La memoria reconoce ambas normas como marco de referencia del ámbito y asume que una eventual evolución hacia un producto real requeriría un análisis de conformidad mucho más profundo que el presentado en este trabajo.

En tercer lugar, el sistema mantiene una comunicación constante entre el servidor y el navegador del cliente, a través de la cual viajan credenciales de acceso y datos de las consultas. Estas comunicaciones deben protegerse mediante el protocolo HTTPS, que se fundamenta en el estándar TLS (IETF, 2018) y cifra el contenido de la comunicación, de modo que ni las credenciales ni los datos transmitidos puedan ser leídos por un tercero durante el tránsito por la red. Conviene precisar dónde termina ese cifrado cuando el servicio se publica mediante un túnel, como se describe en el apartado 11.1. En el modelo habitual, el certificado TLS termina en el servidor que aloja la aplicación; con un túnel, el cifrado TLS termina en el borde del proveedor del túnel, y el tramo entre ese borde y el servidor local viaja por el canal cifrado que el propio túnel establece. Esto significa que el proveedor del túnel actúa como extremo de confianza de la conexión HTTPS y, por tanto, debe tratarse como un tercero que puede inspeccionar el tráfico que no está cifrado de extremo a extremo. Esta circunstancia no invalida la protección de las comunicaciones, pero obliga a tener presente que la confianza no termina en el servidor de la aplicación, sino en el operador del túnel.

En cuarto lugar, dado que se trata de una aplicación web accesible desde Internet, la seguridad de la aplicación se fundamenta en el catálogo de riesgos de aplicaciones web de OWASP. OWASP es una organización internacional sin ánimo de lucro dedicada a la seguridad del software, y su publicación más conocida, el Top 10, reúne los diez riesgos de seguridad más críticos que afectan a las aplicaciones web —inyección de código, exposición de datos sensibles, falsificación de peticiones entre sitios, entre otros— (OWASP, 2021). Este catálogo guía las medidas de protección implementadas en el sistema, que incluyen el cifrado de contraseñas, la gestión segura de sesiones, la protección frente a la falsificación de peticiones entre sitios, la limitación de peticiones y el establecimiento de cabeceras de seguridad.

En quinto lugar, el código del sistema se desarrolla íntegramente en Python y debe seguir la guía de estilo PEP 8. Una guía de estilo es un conjunto de convenciones sobre cómo escribir el código —nombres de variables, sangrado, longitud de las líneas, organización de las importaciones— con el fin de que el código sea coherente, legible y fácil de mantener. PEP 8 es un Python Enhancement Proposal, un documento oficial de la comunidad Python: fue redactado originalmente por Guido van Rossum, Barry Warsaw y Nick Coghlan y es mantenido y publicado por la Python Software Foundation, donde se actualiza (van Rossum, Warsaw, & Coghlan, 2001; Python Software Foundation, 2024). En un proyecto de estas dimensiones, donde numerosos módulos interactúan entre sí, la legibilidad del código es un requisito de calidad imprescindible.

Por último, la documentación del proyecto se rige por la normativa de Trabajo Fin de Grado de la Escuela Politécnica Superior de la Universidad Pablo de Olavide, que establece la estructura, el formato y los requisitos formales que deben cumplir los documentos entregables asociados a este TFG (Universidad Pablo de Olavide, 2014). La Tabla 17 resume los estándares y normativas aplicables al sistema.

| Estándar / Norma | Ámbito de aplicación |
|---|---|
| RGPD (Reglamento UE 2016/679) | Protección de datos y tratamiento de información biomédica. |
| LOPDGDD (Ley Orgánica 3/2018) | Adaptación del RGPD al ordenamiento jurídico español. |
| MDR (Reglamento UE 2017/745) | Requisitos de los productos sanitarios destinados a un fin médico. |
| Reglamento de IA (Reglamento UE 2024/1689) | Clasificación y obligaciones de los sistemas de inteligencia artificial. |
| HTTPS / TLS | Protocolo seguro de comunicación entre cliente y servidor. |
| OWASP Top 10 | Seguridad de las aplicaciones web. |
| PEP 8 | Guía de estilo y nomenclatura del código Python. |
| Normativa TFG EPS-UPO | Estructura y formato de la documentación del proyecto. |

*Tabla 17 - Estándares y normativas aplicables al sistema*

## 11.3 Perfiles de usuario del sistema

Identificar correctamente a los usuarios que van a utilizar el sistema es una tarea fundamental dentro del análisis, porque determina desde qué perspectivas se diseña el sistema y qué funcionalidades debe ofrecer a cada tipo de actor. En este apartado conviene distinguir dos planos complementarios que con frecuencia se confunden. El primero es el análisis de los perfiles de usuario, que caracteriza a los colectivos que usarán la plataforma por sus necesidades y por su actividad. El segundo es el modelo de autorización, que define los roles de acceso mediante los que se controla qué puede hacer cada cuenta. Ambos planos se describen a continuación: los perfiles de usuario, en primer lugar, y los roles de acceso, a continuación.

El plan de proyecto identifica dos colectivos de usuarios finales a los que se dirige vitalXAI. El primero lo forman los **facultativos e investigadores clínicos**, el objetivo último del despliegue: profesionales que incorporarían el diagnóstico asistido a su rutina médica e investigadora diaria. Sus necesidades operativas dictan la utilidad real del sistema: obtener un diagnóstico claro y rápido sobre la radiografía, comprender los motivos que lo sustentan mediante los mapas de explicabilidad, poder descargar un informe y disponer de un laboratorio para configurar, comparar y evaluar modelos sin necesidad de escribir código. El segundo colectivo es el **Laboratorio Synergia**, identificado en el plan como usuario externo y primer escalón de adopción: sus líneas de investigación convergen con los objetivos de vitalXAI, por lo que actúa como probador empírico de la herramienta, y sus observaciones condicionan el refinamiento de la interfaz y de los flujos de trabajo. Ninguno de estos colectivos dispone de formación técnica en programación o en aprendizaje automático, de modo que la facilidad de uso y la claridad de la interfaz son requisitos transversales de su adopción, tal y como recoge el requisito RNF-013.

Una decisión de diseño relevante es que la plataforma no restringe el acceso en función del perfil profesional: cualquier usuario con una cuenta puede utilizar tanto la interfaz de diagnóstico como el laboratorio de entrenamiento. Esta decisión simplifica el modelo de acceso, pero tiene una consecuencia de primer orden que debe analizarse. Significa que cualquier facultativo o investigador autenticado puede lanzar entrenamientos que consumen la GPU del servidor durante horas y compiten por la cola de trabajos, por lo que un uso intensivo del laboratorio puede afectar a la experiencia del resto de los usuarios. La garantía de que un entrenamiento no deje la plataforma inaccesible para el resto se apoya en la ejecución asíncrona y en la cola persistente de trabajos (OBJ-010), y queda recogida en el requisito RNF-017, que exige que el servicio permanezca disponible y operativo durante las tareas de larga duración. No obstante, conviene reconocer el límite de esta solución: la interfaz permanece operativa porque las peticiones se encolan, pero los entrenamientos compiten por los recursos computacionales de la estación de trabajo descrita en el apartado 11.1, y una saturación prolongada de la GPU puede degradar el tiempo de respuesta de los diagnósticos que se procesan simultáneamente. El análisis asume este compromiso y lo señala como un punto de evolución: una solución futura debería valorar mecanismos de priorización de trabajos o de limitación de entrenamientos concurrentes por cuenta.

Sobre los perfiles anteriores se define el modelo de autorización, que materializa el control de acceso mediante tres roles. El **usuario visitante** representa a todas las personas que acceden a la aplicación sin haberse autenticado; su acceso se limita a las funcionalidades públicas del sistema: la creación de una nueva cuenta, el inicio de sesión y el cambio de idioma de la interfaz. El **usuario autenticado** es el perfil central del sistema: agrupa a todos los profesionales con cuenta registrada, con independencia de que su actividad sea fundamentalmente clínica o investigadora, y cubre la totalidad de la funcionalidad no administrativa —diagnóstico, historial, laboratorio MLOps y resultados—. El **usuario administrador** es el responsable del gobierno de la plataforma: gestiona las cuentas y supervisa la actividad registrada, y constituye el único caso en el que el acceso está restringido por rol. Es importante señalar que el administrador es, ante todo, un usuario autenticado: el rol añade capacidades de gobierno, pero no introduce un perfil técnico distinto, de modo que se mantiene la premisa, recogida en RNF-013, de que la plataforma no exige conocimientos técnicos a ninguno de sus usuarios.

La Tabla 18 resume los roles de acceso identificados, con su descripción, el perfil técnico exigido y su nivel de acceso.

| Tipo de usuario | Descripción | Perfil técnico | Nivel de acceso |
|---|---|---|---|
| Usuario visitante | Persona que accede a la plataforma sin autenticarse. | No se exigen conocimientos técnicos. | Registro, inicio de sesión y cambio de idioma. |
| Usuario autenticado | Profesional con cuenta (clínica o investigadora) que utiliza el sistema. | No se exigen conocimientos técnicos. | Acceso completo a la funcionalidad no administrativa: diagnóstico, historial, laboratorio MLOps y resultados. |
| Usuario administrador | Usuario autenticado con capacidades de gobierno sobre la plataforma. | No se exigen conocimientos técnicos. | Gestión de usuarios y supervisión de la actividad. |

*Tabla 18 - Roles de acceso del sistema*

Con la definición de los objetivos del sistema, el contexto tecnológico, la normativa aplicable y los perfiles de usuario, queda delimitado el ámbito del sistema. Sobre este marco, los capítulos siguientes del análisis descomponen el sistema en subsistemas, traducen las necesidades de los usuarios en requisitos y casos de uso, y definen el plan de pruebas que verificará el cumplimiento de lo especificado.

---

## Referencias del capítulo

España. (2018). Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales. *Boletín Oficial del Estado*, 294, 119788-119857.

IETF. (2018). *RFC 8446 – The Transport Layer Security (TLS) Protocol Version 1.3*. Obtenido de https://datatracker.ietf.org/doc/html/rfc8446

OWASP. (2021). *OWASP Top 10:2021 – The ten most critical web application security risks*. Obtenido de https://owasp.org/Top10/

Parlamento Europeo y Consejo de la Unión Europea. (2016). Reglamento (UE) 2016/679 relativo a la protección de las personas físicas en lo que respecta al tratamiento de los datos personales y a la libre circulación de estos datos (RGPD). *Diario Oficial de la Unión Europea*, L119, 1-88.

Parlamento Europeo y Consejo de la Unión Europea. (2017). Reglamento (UE) 2017/745 sobre los productos sanitarios, por el que se modifican la Directiva 2001/83/CE, el Reglamento (CE) n.º 178/2002 y el Reglamento (CE) n.º 1223/2009 y por el que se derogan las Directivas 90/385/CEE y 93/42/CEE del Consejo. *Diario Oficial de la Unión Europea*, L117, 1-175.

Parlamento Europeo y Consejo de la Unión Europea. (2024). Reglamento (UE) 2024/1689 por el que se establecen normas armonizadas en materia de inteligencia artificial y por el que se modifican los Reglamentos (CE) n.º 300/2008, (UE) n.º 167/2013, (UE) n.º 168/2013, (UE) 2018/858, (UE) 2018/1139 y (UE) 2019/2144 y las Directivas 2014/90/UE, (UE) 2016/797 y (UE) 2020/1828 (Reglamento de Inteligencia Artificial). *Diario Oficial de la Unión Europea*, serie L, 12.7.2024.

Python Software Foundation. (2024). *PEP 8 – Style Guide for Python Code*. Obtenido de https://peps.python.org/pep-0008/

Universidad Pablo de Olavide. (2014). *Guía técnica para la realización del Trabajo Fin de Grado en Ingeniería Informática en Sistemas de Información*. Escuela Politécnica Superior.

van Rossum, G., Warsaw, B., & Coghlan, N. (2001). *PEP 8 – Style Guide for Python Code*. Obtenido de https://peps.python.org/pep-0008/

