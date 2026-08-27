# Capítulo 15: Verificación de la consistencia del análisis

El análisis del sistema de vitalXAI ha producido, a lo largo de los capítulos 10 a 14, un conjunto de artefactos complementarios que describen la plataforma desde perspectivas distintas: los objetivos del sistema (capítulo 11) declaran los fines que se persiguen, los requisitos funcionales y no funcionales (capítulo 12) concretan las capacidades y las condiciones de calidad que deben cumplirse, los casos de uso (capítulo 12) describen el comportamiento observable del sistema, los subsistemas de análisis (capítulo 13) agrupan esas capacidades en unidades cohesivas y el modelo de dominio (capítulo 14) identifica las entidades sobre las que todo ese comportamiento se apoya. La utilidad de este conjunto de artefactos depende de que exista una correspondencia coherente entre ellos: si un objetivo no tiene requisitos que lo materialicen, si un requisito no se refleja en ningún caso de uso, o si un caso de uso no tiene entidades del dominio sobre las que operar, el análisis adolecería de lagunas que se propagarían al diseño y, finalmente, al producto construido.

Este capítulo cierra la etapa de análisis realizando una verificación cruzada de la consistencia entre los artefactos producidos. El objetivo no es describir de nuevo el contenido de los capítulos anteriores, sino comprobar, de forma sistemática y verificable, que el modelo conceptual del sistema es completo, coherente y trazable en todas sus dimensiones. Para ello, el capítulo se organiza en tres secciones. La primera examina la coherencia entre los objetivos del sistema y los requisitos que los materializan. La segunda comprueba la cobertura de los requisitos por parte de los casos de uso y la correspondencia entre estos y los subsistemas de análisis. La tercera recoge las decisiones estratégicas de análisis que, derivadas de la verificación anterior, consolidan la estabilidad y la calidad metodológica del modelo y condicionarán las decisiones de diseño de los capítulos siguientes (Larman, 2004; Jacobson, Booch & Rumbaugh, 1999).

## 15.1 Coherencia entre los objetivos del sistema y los requisitos

La primera dimensión de la verificación de consistencia relaciona los objetivos del sistema, declarados en el capítulo 11, con los requisitos funcionales y no funcionales que los materializan. Los once objetivos del sistema (OBJ-001 a OBJ-011) cubren las dimensiones funcionales y de calidad de la plataforma: el diagnóstico asistido con inteligencia artificial explicable (OBJ-001), la gestión del historial de consultas (OBJ-002), la generación de informes descargables (OBJ-003), el laboratorio de entrenamiento MLOps (OBJ-004), la evaluación rigurosa de los modelos (OBJ-005), la reproducibilidad de los experimentos (OBJ-006), el acceso seguro y personalizado al sistema (OBJ-007), la persistencia y trazabilidad de la información (OBJ-008), la usabilidad e internacionalización de la interfaz (OBJ-009), la ejecución asíncrona de tareas de larga duración (OBJ-010) y la administración de la plataforma (OBJ-011).

### 15.1.1 Cobertura de los objetivos por los requisitos funcionales

La matriz de trazabilidad entre requisitos funcionales y objetivos del sistema, presentada en la sección 12.1.1.7 del capítulo 12, permite comprobar la cobertura de los objetivos por los cuarenta y un requisitos funcionales (RF-001 a RF-041). El examen de la matriz confirma que todos los objetivos del sistema quedan cubiertos por al menos un requisito funcional y que todos los requisitos funcionales están justificados por el objetivo al que responden, de modo que no existe ningún objetivo huérfano sin capacidades asociadas ni ninguna capacidad carente de fundamento.

| Objetivo | Requisitos funcionales que lo materializan |
|---|---|
| OBJ-001 Diagnóstico asistido con IA explicable | RF-007, RF-008, RF-009, RF-010, RF-011, RF-012, RF-039 |
| OBJ-002 Gestión del historial de consultas | RF-013, RF-014, RF-015, RF-016 |
| OBJ-003 Generación de informes descargables | RF-030, RF-039 |
| OBJ-004 Laboratorio de entrenamiento MLOps | RF-017, RF-018, RF-019, RF-020, RF-021, RF-030, RF-031, RF-032, RF-041 |
| OBJ-005 Evaluación rigurosa de los modelos | RF-022, RF-023, RF-024, RF-025, RF-026, RF-027, RF-028, RF-029 |
| OBJ-006 Reproducibilidad de los experimentos | RF-020 |
| OBJ-007 Acceso seguro y personalizado al sistema | RF-001, RF-002, RF-003, RF-005, RF-006 |
| OBJ-008 Persistencia y trazabilidad de la información | RF-013, RF-021 |
| OBJ-009 Usabilidad e internacionalización de la interfaz | RF-004, RF-038 |
| OBJ-010 Ejecución asíncrona de tareas de larga duración | RF-010, RF-020, RF-028, RF-036, RF-037, RF-041 |
| OBJ-011 Administración de la plataforma | RF-006, RF-033, RF-034, RF-035, RF-040 |

*Tabla 34 - Cobertura de los objetivos del sistema por los requisitos funcionales*

La tabla 45 resume la asignación de los requisitos funcionales a los objetivos del sistema que ya se detallaba en la matriz de la sección 12.1.1.7. De su lectura se desprende que la distribución es equilibrada y refleja la naturaleza de cada objetivo: los objetivos de carácter funcional, como el diagnóstico asistido (OBJ-001) o la evaluación rigurosa de los modelos (OBJ-005), concentran un número elevado de requisitos, mientras que los objetivos transversales se apoyan en un número menor de requisitos de aplicación general, como el aislamiento de datos entre usuarios (RF-005) en el caso del acceso seguro (OBJ-007) o los requisitos de la cola de trabajos (RF-036 y RF-037) en el de la ejecución asíncrona (OBJ-010). Esta distribución es coherente con el diseño del sistema: las capacidades nucleares requieren una especificación funcional más detallada, mientras que las propiedades transversales se declaran mediante requisitos de aplicación amplia.

### 15.1.2 Cobertura de los objetivos por los requisitos no funcionales

La segunda matriz de la sección 12.1.2.9 del capítulo 12 relaciona los requisitos no funcionales (RNF-001 a RNF-034) con los objetivos del sistema a los que aportan condiciones de calidad. El examen de esta matriz confirma que todos los objetivos con implicaciones transversales de calidad quedan cubiertos por los requisitos no funcionales correspondientes. Los objetivos de carácter puramente funcional —la gestión del historial (OBJ-002) y la generación de informes descargables (OBJ-003)— no presentan asignaciones en esta matriz, pues su consecución se materializa mediante requisitos funcionales; en cambio, el laboratorio de entrenamiento (OBJ-004) y la evaluación rigurosa de los modelos (OBJ-005) sí cuentan con requisitos de calidad asociados, porque la fiabilidad del laboratorio y la corrección de sus resultados dependen de condiciones no funcionales, y no solo de capacidades funcionales.

| Objetivo | Requisitos no funcionales que aportan condiciones de calidad |
|---|---|
| OBJ-001 Diagnóstico asistido con IA explicable | RNF-019 |
| OBJ-004 Laboratorio de entrenamiento MLOps | RNF-022 |
| OBJ-005 Evaluación rigurosa de los modelos | RNF-033, RNF-034 |
| OBJ-006 Reproducibilidad de los experimentos | RNF-033, RNF-034 |
| OBJ-007 Acceso seguro y personalizado al sistema | RNF-001 a RNF-018 |
| OBJ-008 Persistencia y trazabilidad de la información | RNF-031, RNF-032 |
| OBJ-009 Usabilidad e internacionalización de la interfaz | RNF-023, RNF-024, RNF-025, RNF-026 |
| OBJ-010 Ejecución asíncrona de tareas de larga duración | RNF-020, RNF-021, RNF-022, RNF-027, RNF-028, RNF-029, RNF-030 |
| OBJ-011 Administración de la plataforma | RNF-006, RNF-009 |

*Tabla 35 - Cobertura de los objetivos del sistema por los requisitos no funcionales*

La tabla 46 muestra la asignación de los requisitos no funcionales a los objetivos con implicaciones de calidad. La concentración más notable se produce en el objetivo de acceso seguro y personalizado al sistema (OBJ-007), que agrupa los requisitos de seguridad y confidencialidad (RNF-001 a RNF-018), lo que refleja la relevancia que la protección de los datos clínicos tiene en el ámbito sanitario de la plataforma. Le sigue el objetivo de ejecución asíncrona (OBJ-010), con los requisitos de robustez y rendimiento (RNF-020 a RNF-022 y RNF-027 a RNF-030), y el de reproducibilidad (OBJ-006), con los requisitos de reproducibilidad del sistema (RNF-033 y RNF-034). Esta distribución evidencia que las dimensiones de calidad del sistema se concentran, como cabía esperar, en los objetivos con mayor sensibilidad clínica y computacional.

## 15.2 Cobertura de los requisitos por los casos de uso y los subsistemas

La segunda dimensión de la verificación desciende un nivel en la cadena de trazabilidad: comprueba que los requisitos funcionales se materializan en casos de uso y que estos, a su vez, se agrupan en los subsistemas de análisis definidos en el capítulo 13. Esta verificación garantiza que ninguna capacidad declarada en la especificación de requisitos quede sin representación en el comportamiento observable del sistema ni en la estructura de análisis sobre la que se apoyará el diseño.

### 15.2.1 Correspondencia entre requisitos funcionales y casos de uso

La matriz de trazabilidad requisitos-casos de uso de la sección 12.2.4 del capítulo 12, desglosada en cinco tablas, una por módulo funcional, relaciona los cuarenta y un requisitos funcionales con los treinta y nueve casos de uso del sistema. El examen de las matrices confirma la cobertura en ambas direcciones: todos los requisitos funcionales quedan materializados en al menos un caso de uso y todos los casos de uso están justificados por el requisito funcional que los origina. Se cumple además la correspondencia biunívoca declarada en la especificación: la mayoría de los requisitos se materializan en un único caso de uso del mismo módulo, y solo los dos requisitos de carácter transversal —el aislamiento de datos entre usuarios (RF-005) y los roles y el control de acceso (RF-006)— no dan lugar a un caso de uso propio, condicionando el comportamiento del resto de las interacciones en lugar de constituir interacciones independientes.

| Módulo funcional | Requisitos | Casos de uso |
|---|---|---|
| Gestión del acceso y de la cuenta | RF-001 a RF-006 | CU-001 a CU-004 |
| Interfaz de diagnóstico asistido | RF-007 a RF-016, RF-039 | CU-005 a CU-014, CU-037 |
| Laboratorio de experimentación MLOps | RF-017 a RF-032, RF-041 | CU-015 a CU-030, CU-039 |
| Supervisión y administración de la plataforma | RF-033 a RF-035, RF-040 | CU-031 a CU-033, CU-038 |
| Capacidades transversales de la plataforma | RF-036 a RF-038 | CU-034 a CU-036 |

*Tabla 36 - Correspondencia entre los módulos funcionales, los requisitos y los casos de uso*

La tabla 47 resume la correspondencia entre módulos funcionales, requisitos y casos de uso que ya detallaban las cinco matrices de la sección 12.2.4. La distribución de los casos de uso entre los módulos es proporcional a la complejidad funcional de cada uno: el módulo de laboratorio MLOps, el más extenso de la plataforma, concentra diecisiete casos de uso (CU-015 a CU-030 y CU-039) que materializan los diecisiete requisitos del laboratorio (RF-017 a RF-032 y RF-041), el módulo de interfaz de diagnóstico reúne once casos de uso (CU-005 a CU-014 y CU-037), el de administración cuatro (CU-031 a CU-033 y CU-038), y los módulos de acceso y de capacidades transversales se limitan a cuatro y tres casos de uso respectivamente. Esta proporcionalidad es un indicador de la consistencia de la especificación: los ámbitos funcionales que concentran más capacidades son también los que reciben un mayor nivel de detalle en su comportamiento.

### 15.2.2 Correspondencia entre casos de uso y subsistemas de análisis

La descomposición en subsistemas del capítulo 13 agrupa los casos de uso en seis subsistemas de análisis, de modo que cada caso de uso pertenece exactamente a un subsistema y cada requisito funcional queda asignado al subsistema que lo materializa. La correspondencia entre los subsistemas de análisis y los módulos funcionales de requisitos es directa, como se comprobó al construir las fichas de subsistema del capítulo 13: el subsistema de acceso y gestión de cuentas (SS-001) recoge los casos de uso de autenticación (CU-001 a CU-004), el de diagnóstico asistido (SS-002) los del flujo clínico y del informe de la consulta (CU-005 a CU-010 y CU-037), el de gestión del historial (SS-003) los de recuperación y gestión de consultas (CU-011 a CU-014), el de laboratorio MLOps (SS-004) los de experimentación y de limitación de entrenamientos (CU-015 a CU-030 y CU-039), el de supervisión y administración (SS-005) los de administración y gestión de cuentas (CU-031 a CU-033 y CU-038) y el de capacidades transversales (SS-006) los de ejecución asíncrona y personalización (CU-034 a CU-036).

La verificación de esta dimensión revela además dos dependencias estructurales que condicionan el diseño y que ya se señalaron en la síntesis del capítulo 13. En primer lugar, los subsistemas SS-002, SS-003, SS-004 y SS-005 presuponen la existencia de una identidad autenticada establecida por el subsistema de acceso (SS-001), sobre la que se aplican el aislamiento de datos entre usuarios (RF-005) y el control de roles (RF-006). En segundo lugar, los subsistemas SS-002 y SS-004 delegan la ejecución de sus tareas de larga duración —los diagnósticos y los entrenamientos— en el mecanismo de cola de trabajos del subsistema de capacidades transversales (SS-006), que actúa como servicio común de ejecución asíncrona. La existencia de estas dependencias, lejos de ser una inconsistencia, refleja la cohesión del modelo: los subsistemas mantienen una alta cohesión interna y un bajo acoplamiento externo, y las únicas interacciones entre ellos son las estrictamente necesarias para el flujo funcional completo.

### 15.2.3 Cobertura de los requisitos no funcionales por los subsistemas

La cobertura de los requisitos no funcionales presenta una naturaleza distinta a la de los funcionales, puesto que estos requisitos no se materializan en casos de uso ni se asignan a un único subsistema, sino que condicionan de forma transversal el comportamiento de la plataforma. Aun así, es posible verificar que cada grupo de requisitos no funcionales tiene un subsistema que vela de forma principal por su cumplimiento, lo que garantiza que ninguna condición de calidad queda sin responsable en la estructura de análisis.

| Grupo de requisitos no funcionales | Requisitos | Subsistema responsable principal |
|---|---|---|
| Seguridad de la plataforma y del acceso | RNF-001 a RNF-011 | SS-001 Acceso y gestión de cuentas |
| Confidencialidad y protección de los datos | RNF-012 a RNF-018 | SS-001 Acceso y gestión de cuentas |
| Rendimiento y capacidad de respuesta | RNF-019 a RNF-022 | SS-002 Diagnóstico asistido |
| Sencillez de uso y accesibilidad | RNF-023 a RNF-026 | SS-006 Capacidades transversales |
| Robustez y disponibilidad del servicio | RNF-027 a RNF-030 | SS-006 Capacidades transversales |
| Persistencia y salvaguarda de los datos | RNF-031, RNF-032 | SS-001 Acceso y gestión de cuentas |
| Reproducibilidad del sistema | RNF-033, RNF-034 | SS-004 Laboratorio MLOps |
| Documentación y entregables | RNF-037, RNF-038 | Transversal a toda la plataforma |

*Tabla 37 - Asignación de los grupos de requisitos no funcionales a los subsistemas*

La tabla 48 recoge la asignación de los grupos de requisitos no funcionales al subsistema que vela de forma principal por su cumplimiento. La asignación se ha realizado atendiendo al ámbito funcional en el que cada grupo produce su efecto: la seguridad y la confidencialidad se asocian al subsistema que establece la identidad y la sesión (SS-001), el rendimiento de la inferencia al subsistema que ejecuta los diagnósticos (SS-002), la sencillez de uso, la robustez y la disponibilidad al subsistema que provee los servicios transversales y la cola de trabajos (SS-006), y la reproducibilidad al subsistema que orquesta la experimentación (SS-004). El grupo de documentación y entregables se declara transversal, puesto que la documentación y el manual de usuario afectan al conjunto de la plataforma y no a un subsistema concreto.

## 15.3 Decisiones estratégicas del análisis

La verificación de consistencia realizada en las secciones anteriores confirma la integridad del modelo de análisis de vitalXAI: todos los objetivos tienen requisitos que los materializan, todos los requisitos funcionales se reflejan en casos de uso, todos los casos de uso se agrupan en subsistemas y todos los grupos de requisitos no funcionales tienen un subsistema responsable. Superada esta verificación, conviene consolidar las decisiones estratégicas que el análisis ha adoptado y que, por su alcance transversal, condicionarán las decisiones de diseño de los capítulos siguientes. Estas decisiones son el resultado de un proceso dirigido por requisitos y objetivos, en línea con el enfoque metodológico descrito en el capítulo 10, y su justificación se apoya en los artefactos producidos a lo largo de la etapa de análisis (Jacobson, Booch & Rumbaugh, 1999; Larman, 2004).

**Arquitectura modular por subsistemas.** El dominio se ha dividido en seis subsistemas de análisis con alta cohesión y bajo acoplamiento, de modo que la plataforma pueda extenderse en el futuro. Esta separación asegura que la evolución de un ámbito funcional —por ejemplo, la incorporación de nuevas arquitecturas de deep learning en el laboratorio de experimentación— no implique modificar la lógica de presentación, la gestión de usuarios o la supervisión administrativa. La correspondencia biunívoca entre los subsistemas y los módulos funcionales de requisitos garantiza, además, que el cambio de un subsistema afecte únicamente a los requisitos y casos de uso de su ámbito.

**Aislamiento de datos y control de acceso como requisitos transversales.** El aislamiento de datos entre usuarios (RF-005) y los roles y el control de acceso (RF-006) se han declarado como requisitos transversales que condicionan el comportamiento de todos los subsistemas, materializándose en el subsistema de acceso (SS-001) que establece la identidad sobre la que ambos se aplican. Esta decisión, coherente con la entidad raíz Usuario del modelo de dominio del capítulo 14, garantiza que cada usuario solo accede a sus propias consultas, sesiones y datos, y que las operaciones de administración quedan restringidas al rol correspondiente.

**Ejecución asíncrona de las tareas de larga duración.** Los diagnósticos, los entrenamientos y las validaciones externas se ejecutan de forma asíncrona mediante un mecanismo de cola de trabajos, desacoplado de la interfaz. Esta decisión, declarada en el objetivo OBJ-010 y en los requisitos de robustez y capacidad de respuesta (RNF-020 a RNF-022 y RNF-027 a RNF-030), preserva la capacidad de respuesta de la aplicación web: el procesamiento de una radiografía o el entrenamiento de un modelo no bloquea el hilo principal de la navegación, y el usuario continúa interactuando con la plataforma mientras el trabajo se procesa en segundo plano, siendo notificado cuando el resultado queda disponible.

**Explicabilidad integrada en el flujo clínico y en el laboratorio.** La explicabilidad no se ha concebido como un módulo aislado, sino como una capacidad integrada tanto en el diagnóstico asistido —cada consulta se acompaña de sus mapas de explicabilidad (Saliency Maps, SmoothGrad y Grad-CAM, o mapas de atención para arquitecturas Transformer)— como en el laboratorio de experimentación —cada modelo entrenado se somete a un análisis de explicabilidad—. Esta decisión materializa el objetivo OBJ-001 y constituye el fundamento de la confianza clínica en el sistema: el profesional no solo recibe la predicción, sino los motivos que la justifican, de modo que pueda verificar que el modelo se fija en las regiones pulmonares relevantes.

**Modelo de dominio centrado en las entidades de negocio.** El modelo de dominio del capítulo 14 identifica ocho clases de negocio que responden directamente a los módulos funcionales y a los casos de uso del capítulo 12, de modo que cada entidad tiene una correspondencia clara con las capacidades declaradas en la especificación. Las decisiones de modelado adoptadas —la consolidación de los parámetros del experimento interpretados por el asistente en la clase ModeloEntrenado, con la ruta del dataset en la sesión de experimentación, y el establecimiento de Usuario como entidad raíz— simplifican el modelo sin perder capacidad expresiva y garantizan la coherencia entre el comportamiento dinámico descrito en las secuencias de interacción y la estructura estática sobre la que se apoya.

**Persistencia y reproducibilidad de la experimentación.** El laboratorio de entrenamiento registra de forma persistente las sesiones, los modelos, los resultados y la configuración de los experimentos, de modo que el investigador pueda recuperar, comparar y reproducir sus experimentos. Esta decisión materializa los objetivos de reproducibilidad (OBJ-006) y de persistencia y trazabilidad (OBJ-008), y se apoya en los requisitos no funcionales de reproducibilidad y de integridad de la persistencia (RNF-031, RNF-033 y RNF-034), que condicionarán las decisiones de diseño de la capa de datos y del pipeline de entrenamiento.

Con estas decisiones, el análisis de vitalXAI queda cerrado de forma consistente y trazable en todas sus dimensiones. Los artefactos producidos en los capítulos 10 a 14 —objetivos, requisitos, casos de uso, subsistemas y modelo de dominio— constituyen la base sobre la que se adoptarán las decisiones de diseño del sistema en los capítulos siguientes, de modo que la transición del análisis al diseño se realiza sobre un modelo verificado y sin lagunas de cobertura.

---

## Referencias del capítulo

Jacobson, I., Booch, G., & Rumbaugh, J. (1999). *The Unified Software Development Process*. Addison-Wesley.

Larman, C. (2004). *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3rd ed.). Prentice Hall.