# Capítulo 11: Definición del ámbito del sistema

El contexto y el estado del arte en el que se inscribe vitalXAI se presentaron en el capítulo 1, donde se describieron el problema de la neumonía, la radiografía de tórax como imagen digital, la evolución del aprendizaje profundo aplicado al diagnóstico por imagen, los conjuntos de datos y los modelos de referencia, y las plataformas MLOps existentes. Este capítulo no repite ese análisis: asume lo allí expuesto y se centra en delimitar el ámbito del sistema, es decir, qué capacidades incluye vitalXAI como producto, bajo qué entorno tecnológico, con qué normativa y para qué usuarios.

El capítulo delimita el alcance funcional de vitalXAI y las condiciones generales en las que debe operar. No incorpora una revisión bibliográfica ni compara soluciones existentes, porque esa fundamentación ya se encuentra en el capítulo 1.

La plataforma se concibe como una aplicación web de servidor. El usuario final accede mediante un navegador y no necesita instalar componentes locales. La infraestructura de ejecución sí requiere un entorno compatible con el motor de aprendizaje automático, capacidad de cómputo acelerado y almacenamiento para los datos y artefactos del sistema. Estas condiciones se analizan en el apartado de contexto tecnológico, mientras que las tecnologías concretas se justifican en los capítulos 17 y 23.

Desde el punto de vista funcional, el alcance se organiza en dos núcleos: el diagnóstico asistido y el laboratorio de experimentación MLOps. Ambos se complementan con capacidades transversales de autenticación, aislamiento de datos, ejecución asíncrona, internacionalización y administración. La definición formal de estas capacidades comienza con los objetivos del sistema y continúa con los requisitos y casos de uso del análisis.

## Objetivos del sistema

Los objetivos del sistema describen lo que vitalXAI debe ofrecer como producto. Se obtienen a partir de las reuniones mantenidas con el tutor y de los objetivos generales del proyecto, y sirven de base para los requisitos de los capítulos siguientes. Cada objetivo se presenta mediante una ficha con su identificador, nombre, descripción, importancia y estado. Estos objetivos se diferencian de los objetivos del plan de proyecto, que describen lo que el alumno debe conseguir durante el desarrollo. La tabla 15 relaciona ambos tipos de objetivos.

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

Los resultados de un diagnóstico no deben quedarse en la pantalla: el profesional necesita un documento que pueda archivar, imprimir o incorporar a su flujo de trabajo habitual. Este objetivo cubre la generación de informes en formato PDF. El informe consolidado de una sesión de entrenamiento está formalizado en el requisito RF-030, que fija su contenido (configuración del experimento, ranking de modelos, comparativas estadísticas, validación externa y métricas de explicabilidad y calibración). El informe individual de un diagnóstico se formaliza en el requisito RF-039 y se verifica en la prueba PU-017.

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
| Comentarios | El informe de sesión se formaliza en RF-030 y el informe individual del diagnóstico en RF-039. La implementación del informe individual se verifica en PU-017. |

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

El sistema debe permitir comparar el rendimiento de los modelos y observar su comportamiento sobre una cohorte independiente. Este objetivo incluye la evaluación estadística, la validación externa y la presentación de los resultados de forma comprensible para el investigador. Los contrastes deben interpretarse teniendo en cuenta las limitaciones del protocolo experimental.

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

La reproducibilidad es especialmente relevante en el aprendizaje automático, donde una inicialización aleatoria o un orden de datos diferente pueden alterar los resultados. Este objetivo busca asociar cada experimento con su configuración y sus semillas aleatorias, de modo que los resultados puedan verificarse y repetirse bajo las mismas condiciones (Varoquaux & Cheplygina, 2019).

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
| Comentarios | Este objetivo responde a las limitaciones de reproducibilidad identificadas en la literatura sobre aprendizaje automático (Varoquaux & Cheplygina, 2019). |

*Tabla 9 - OBJ-006: Reproducibilidad de los experimentos*

**OBJ-007 – Acceso seguro y personalizado al sistema.**

El sistema trata información de carácter clínico, aunque anonimizada, y cada usuario debe disponer de un espacio de trabajo aislado. Este objetivo cubre el registro, la autenticación, el cierre de sesión y el acceso de cada profesional a sus propios datos. El modelo de autorización distingue estas operaciones de las funciones de gobierno reservadas al administrador, que se recogen en el OBJ-011.

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
| Comentarios | La autenticación es necesaria por el carácter clínico de los datos gestionados. El mecanismo concreto de autenticación corresponde al diseño. |

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

El sistema está pensado para usuarios sin formación técnica, por lo que la interfaz debe permitir completar las operaciones sin interactuar con código ni con entornos de programación. Además, debe estar disponible en varios idiomas para que el usuario pueda cambiar de idioma de forma dinámica.

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
| Comentarios | La usabilidad orienta el diseño de la interfaz, pero no determina la corrección funcional de los modelos. |

*Tabla 12 - OBJ-009: Usabilidad e internacionalización de la interfaz*

**OBJ-010 – Ejecución asíncrona de tareas de larga duración.**

El entrenamiento de un modelo de deep learning puede prolongarse durante horas. Este objetivo establece que los entrenamientos, los análisis de explicabilidad y la validación externa se ejecuten de forma asíncrona mediante una cola de trabajos, para que el usuario pueda consultar el estado de cada tarea sin mantener abierta la petición inicial.

| Campo | Contenido |
|---|---|
| ID | OBJ-010 |
| Nombre | Ejecución asíncrona de tareas de larga duración |
| Versión | 01 |
| Autores | Luis Carmona Berdugo |
| Fuente | Reunión de inicio con el tutor |
| Descripción | El sistema debe ejecutar de forma asíncrona las tareas de larga duración, como entrenamientos, análisis de explicabilidad y validación externa, para que la interfaz permanezca operativa durante su ejecución y el usuario pueda consultar el estado de cada tarea. |
| Importancia | Media |
| Estado | Aprobado |
| Comentarios | Este objetivo favorece la disponibilidad de la plataforma durante los procesos computacionales más costosos. |

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
| OBJ-009 Usabilidad e internacionalización | OE8, OE11 | La interfaz aborda la usabilidad (OE8) y el soporte multilingüe corresponde a OE11. |
| OBJ-010 Ejecución asíncrona de tareas | OE10 | El procesamiento asíncrono (OE10) se materializa en este objetivo. |
| OBJ-011 Administración de la plataforma | No aplica | Sin objetivo específico directo: la administración amplía el alcance planificado y se apoya, para el rol, en el control de acceso (OE3). |

*Tabla 15 - Correspondencia entre los objetivos del sistema y los objetivos específicos del plan de proyecto*

## 11.1 Contexto tecnológico y restricciones de entorno
El sistema se desarrolla sobre un entorno tecnológico que establece determinadas condiciones de trabajo. Este apartado distingue entre las restricciones que condicionan el diseño y las decisiones tecnológicas propias del proyecto, que se justifican en la parte de diseño de la memoria.

La principal restricción del entorno es la compatibilidad con Python, lenguaje utilizado por las librerías de aprendizaje automático, los formatos de los modelos y las herramientas de evaluación del proyecto. Por ello, el entorno de ejecución debe mantener la compatibilidad con ese ecosistema.

El entrenamiento requiere capacidad de cómputo acelerado mediante GPU, especialmente cuando se ejecuta validación cruzada sobre arquitecturas de mayor tamaño. El proyecto utiliza un equipo portátil con una GPU NVIDIA RTX 4060 Laptop y 8 GB de VRAM. Esta infraestructura permite realizar las ejecuciones previstas con tamaños de lote reducidos y precisión mixta, aunque el tiempo disponible limita el número de experimentos que pueden completarse.

El equipo forma parte de la infraestructura ya disponible y su amortización no se imputa al coste del TFG. Se descartó contratar instancias en la nube por el coste asociado y porque el trabajo local permite disponer de los pesos y los datos sin depender de un servicio externo. Como consecuencia, los tiempos de entrenamiento deben estimarse con prudencia y los experimentos más costosos deben programarse con antelación.

Sobre estas restricciones, el sistema opera con un servicio web, un motor de aprendizaje automático, una base de datos relacional y un asistente conversacional conectado a un servicio externo. La elección de los frameworks, las librerías y sus versiones corresponde al diseño. En el análisis solo se fija el contexto tecnológico resumido en la tabla 16.

| Aspecto del entorno | Contexto relevante para el análisis |
|---|---|
| Lenguaje y entorno de ejecución | Python y un entorno compatible con las librerías de aprendizaje automático. |
| Aplicación web | Aplicación servidor accesible desde un navegador. |
| Persistencia | Base de datos relacional para cuentas, consultas, sesiones y trabajos. |
| Aprendizaje automático | Frameworks de deep learning para arquitecturas convolucionales y basadas en atención. |
| Procesamiento y evaluación | Herramientas Python para preparar datos, calcular métricas y generar representaciones. |
| Asistente conversacional | Servicio externo de inferencia lingüística integrado mediante una API. |

*Tabla 16 - Contexto tecnológico del sistema*

La tabla anterior recoge el contexto tecnológico de trabajo, no la especificación de implementación. Las tecnologías concretas, las versiones de las dependencias, las librerías de seguridad y las herramientas de calidad y pruebas se seleccionan y justifican en la parte de diseño, especialmente en los capítulos 17 y 23.

En cuanto al despliegue, el sistema debe poder publicarse desde la máquina de ejecución y ser accesible mediante un navegador. La forma concreta de exponer el servicio, el proveedor utilizado y las alternativas descartadas son decisiones de diseño y se documentan en los capítulos 17 y 23. En este capítulo solo se establece que el acceso remoto debe protegerse mediante un canal cifrado y que la infraestructura local no debe exponer directamente sus servicios internos.

En cuanto a la reproducibilidad, la fijación de versiones y el aislamiento del entorno reducen una fuente de variabilidad, pero no garantizan resultados idénticos en todas las ejecuciones. Como se señala en el objetivo OBJ-006, se busca que los resultados puedan verificarse y repetirse bajo las mismas condiciones, no un determinismo bit a bit. La gestión de las dependencias se orienta a mantener un entorno coherente y reconstruible.

En definitiva, la elección de Python y la disponibilidad de una GPU son restricciones del entorno actual del proyecto. El framework web, la base de datos, las librerías de seguridad, las versiones concretas y el mecanismo de despliegue son decisiones de diseño que se justifican en los capítulos correspondientes.

## 11.2 Normativa y estándares de referencia

El desarrollo del sistema está condicionado por normas y estándares relacionados con la protección de datos, el ámbito sanitario, la seguridad de las comunicaciones, la calidad del código y la documentación del TFG. A continuación se resume su relación con el proyecto.

En primer lugar, el sistema gestiona cuentas de usuarios e imágenes de origen médico. Cuando estos datos permiten identificar a una persona, pueden quedar sujetos a las categorías especiales previstas en el artículo 9 del Reglamento General de Protección de Datos (RGPD). El proyecto utiliza datasets públicos y anonimizados, aplica la minimización de la información y limita el acceso mediante cuentas y roles (Parlamento Europeo y Consejo de la Unión Europea, 2016; España, 2018). El acceso administrativo a datos de otros usuarios se limita a las funciones de supervisión descritas en el requisito RF-005 y en los requisitos RF-033 a RF-035.

Conviene ser preciso sobre la anonimización. El proyecto asume que las imágenes que llegan al sistema están anonimizadas y que los conjuntos de datos utilizados son públicos y anónimos, pero esa asunción no equivale a una garantía implementada: si un facultativo sube una radiografía con identificadores visibles en la imagen o con metadatos DICOM que revelen la identidad del paciente, el sistema los almacena junto con la imagen. En el estado actual del proyecto no existe un mecanismo que despoje automáticamente esos metadatos ni una validación que compruebe la ausencia de identificadores antes de aceptar una carga. Esta circunstancia debe documentarse como una limitación: la anonimización previa recae hoy en el responsable de la captura, y una evolución del sistema debería incorporar la limpieza de metadatos y la detección de identificadores como requisitos explícitos.

El asistente conversacional del laboratorio envía a la API de Groq los mensajes utilizados para configurar un experimento. Aunque esos mensajes se orientan a parámetros técnicos y no a datos clínicos, existe una comunicación con un proveedor externo. Por ello, el despliegue debe documentar el tratamiento y revisar las condiciones aplicables al proveedor.

En segundo lugar, el sistema se inscribe en el ámbito de las tecnologías sanitarias y de la inteligencia artificial. El marco regulatorio aplicable al tratamiento de radiografías, a la posible consideración del software como producto sanitario y a la clasificación futura del sistema de IA se desarrolla en el capítulo 9. En el alcance actual, vitalXAI se limita a un prototipo académico de investigación, sin intención de comercialización ni puesta en servicio clínica.

En tercer lugar, el sistema mantiene una comunicación constante entre el servidor y el navegador del cliente, a través de la cual viajan credenciales de acceso y datos de las consultas. Estas comunicaciones deben protegerse mediante el protocolo HTTPS, que se fundamenta en el estándar TLS (IETF, 2018) y cifra el contenido de la comunicación, de modo que ni las credenciales ni los datos transmitidos puedan ser leídos por un tercero durante el tránsito por la red. Conviene precisar dónde termina ese cifrado cuando el servicio se publica mediante un túnel, como se describe en el apartado 11.1. En el modelo habitual, el certificado TLS termina en el servidor que aloja la aplicación; con un túnel, el cifrado TLS termina en el borde del proveedor del túnel, y el tramo entre ese borde y el servidor local viaja por el canal cifrado que el propio túnel establece. Esto significa que el proveedor del túnel actúa como extremo de confianza de la conexión HTTPS y, por tanto, debe tratarse como un tercero que puede inspeccionar el tráfico que no está cifrado de extremo a extremo. Esta circunstancia no invalida la protección de las comunicaciones, pero obliga a tener presente que la confianza no termina en el servidor de la aplicación, sino en el operador del túnel.

En cuarto lugar, dado que se trata de una aplicación web accesible desde Internet, la seguridad de la aplicación se fundamenta en el catálogo de riesgos de aplicaciones web de OWASP. OWASP es una organización internacional sin ánimo de lucro dedicada a la seguridad del software, y su publicación más conocida, el Top 10, reúne los diez riesgos de seguridad más críticos que afectan a las aplicaciones web, como la inyección de código, la exposición de datos sensibles y la falsificación de peticiones entre sitios (OWASP, 2021). Este catálogo guía las medidas de protección implementadas en el sistema, que incluyen el cifrado de contraseñas, la gestión segura de sesiones, la protección frente a la falsificación de peticiones entre sitios, la limitación de peticiones y el establecimiento de cabeceras de seguridad.

En quinto lugar, el código del sistema se desarrolla íntegramente en Python y debe seguir la guía de estilo PEP 8. Una guía de estilo reúne convenciones sobre nombres de variables, sangrado, longitud de las líneas y organización de las importaciones para mantener un código coherente y legible. PEP 8 es un Python Enhancement Proposal, un documento de la comunidad Python redactado originalmente por Guido van Rossum, Barry Warsaw y Nick Coghlan y publicado por la Python Software Foundation (van Rossum, Warsaw, & Coghlan, 2001; Python Software Foundation, 2024). En este proyecto, el cumplimiento se revisa mediante herramientas de análisis estático.

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

El plan de proyecto identifica dos colectivos de usuarios objetivo a los que se dirige vitalXAI. El primero lo forman los **facultativos e investigadores clínicos**, profesionales que podrían incorporar el diagnóstico asistido a su rutina médica e investigadora. Sus necesidades sirven como referencia para definir el alcance del sistema: obtener un diagnóstico claro sobre la radiografía, comprender los motivos que lo sustentan mediante los mapas de explicabilidad, descargar un informe y disponer de un laboratorio para configurar, comparar y evaluar modelos sin necesidad de escribir código. El segundo colectivo es el **Laboratorio Synergia**, cuyas líneas de investigación son afines a los objetivos de vitalXAI y representan un posible entorno de adopción. Ninguno de estos colectivos participó en sesiones de uso o evaluaciones durante el proyecto, por lo que la facilidad de uso y la claridad de la interfaz se mantienen como requisitos de diseño, no como propiedades validadas empíricamente.

Una decisión de diseño relevante es que la plataforma no restringe el acceso en función del perfil profesional: cualquier usuario con una cuenta puede utilizar tanto la interfaz de diagnóstico como el laboratorio de entrenamiento. Esta decisión simplifica el modelo de acceso, pero implica que cualquier facultativo o investigador autenticado puede lanzar entrenamientos que consumen la GPU del servidor durante horas y compiten por la cola de trabajos. Un uso intensivo del laboratorio puede afectar a la experiencia del resto de los usuarios. La ejecución asíncrona y la cola persistente de trabajos permiten que las peticiones no queden bloqueadas (OBJ-010), aunque no eliminan la competencia por los recursos computacionales. Una saturación prolongada de la GPU puede degradar el tiempo de respuesta de los diagnósticos procesados simultáneamente. La limitación de entrenamientos concurrentes o la priorización de trabajos queda como posible evolución.

Sobre los perfiles anteriores se define el modelo de autorización, que materializa el control de acceso mediante tres roles. El **usuario visitante** accede a la aplicación sin autenticarse y solo puede utilizar las funciones públicas de registro, inicio de sesión y cambio de idioma. El **usuario autenticado** agrupa a los profesionales con cuenta registrada y puede utilizar la funcionalidad no administrativa de diagnóstico, historial, laboratorio MLOps y resultados. El **usuario administrador** es un usuario autenticado con capacidades adicionales de gobierno sobre las cuentas y la actividad de la plataforma. Ninguno de estos roles exige conocimientos técnicos específicos, de acuerdo con el requisito RNF-013.

La Tabla 18 resume los roles de acceso identificados, con su descripción, el perfil técnico exigido y su nivel de acceso.

| Tipo de usuario | Descripción | Perfil técnico | Nivel de acceso |
|---|---|---|---|
| Usuario visitante | Persona que accede a la plataforma sin autenticarse. | No se exigen conocimientos técnicos. | Registro, inicio de sesión y cambio de idioma. |
| Usuario autenticado | Profesional con cuenta (clínica o investigadora) que utiliza el sistema. | No se exigen conocimientos técnicos. | Acceso completo a la funcionalidad no administrativa: diagnóstico, historial, laboratorio MLOps y resultados. |
| Usuario administrador | Usuario autenticado con capacidades de gobierno sobre la plataforma. | No se exigen conocimientos técnicos. | Gestión de usuarios y supervisión de la actividad. |

*Tabla 18 - Roles de acceso del sistema*

Con la definición de los objetivos del sistema, el contexto tecnológico, la normativa aplicable y los perfiles de usuario, queda delimitado el ámbito del sistema. Sobre este marco, los capítulos siguientes del análisis descomponen el sistema en subsistemas, traducen las necesidades de los usuarios en requisitos y casos de uso, y definen el plan de pruebas que verificará el cumplimiento de lo especificado.
