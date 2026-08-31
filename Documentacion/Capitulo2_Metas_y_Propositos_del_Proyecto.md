# Capítulo 2: Metas y Propósitos del Proyecto

Este Trabajo Fin de Grado parte de la necesidad de reunir en un mismo entorno el diagnóstico asistido por inteligencia artificial, la explicabilidad de las predicciones y la evaluación de los modelos. En la práctica, estas capacidades suelen aparecer separadas entre repositorios de código, cuadernos de experimentación y plataformas cerradas, lo que puede dificultar la reproducción de los procedimientos y la inspección de los métodos utilizados (Liu & al., 2019; Varoquaux & Cheplygina, 2019). Aunque diversos estudios han mostrado resultados prometedores en imagen médica, esos resultados dependen de los datos, del protocolo y del entorno de evaluación empleados (Esteva & al., 2017; De Fauw & al., 2018; McKinney & al., 2020). La literatura también advierte de que la aplicación clínica requiere validación rigurosa, análisis estadístico y una exposición clara de las limitaciones (Nagendran & al., 2020; Kelly & al., 2019; Aggarwal & al., 2021). En este contexto se plantea vitalXAI como una plataforma experimental y de apoyo, no como un producto sanitario certificado.

Este capítulo define los fines del proyecto. Primero se presenta el objetivo general y, después, los objetivos específicos que lo descomponen en metas de carácter científico, metodológico y técnico. Los objetivos describen el resultado y el alcance previstos, mientras que las decisiones sobre arquitecturas, técnicas e implementación se justifican en los capítulos correspondientes de análisis, diseño y codificación.

El objetivo general de este Trabajo Fin de Grado es desarrollar vitalXAI, una plataforma web MLOps que integre inteligencia artificial explicable para el diagnóstico asistido de neumonía mediante radiografías de tórax. La plataforma debe reunir en un mismo entorno la ejecución de diagnósticos, la comparación de arquitecturas y la evaluación de las explicaciones generadas por los modelos, con criterios de reproducibilidad y trazabilidad. Su orientación es experimental y de apoyo a la investigación. La interfaz se diseña para que profesionales sanitarios e investigadores puedan utilizar estas capacidades sin necesidad de programar, sin que ello convierta la plataforma en un producto sanitario certificado ni permita sustituir la valoración clínica.

Del objetivo general se derivan once objetivos específicos. Se organizan en dos bloques. El primero, científico y metodológico, reúne la fundamentación teórica, el diseño experimental y la evaluación de los modelos. El segundo, relacionado con la ingeniería web, reúne la construcción de la plataforma, su interfaz, su seguridad, su usabilidad y los servicios que ofrece al usuario.

OE1: Revisar el estado del arte. Analizar la literatura científica sobre la aplicación de la inteligencia artificial al diagnóstico por imagen médica, con especial atención a la detección de neumonía mediante radiografías de tórax, los métodos de inteligencia artificial explicable y las prácticas de MLOps para gestionar el ciclo de vida de los modelos. Esta revisión, realizada en la tarea 0.2 del Sprint 0, sirve de base para las decisiones de diseño e implementación. También permite situar el proyecto frente al estudio de Kermany y colaboradores (Kermany & al., 2018) y considerar aspectos como la calibración, la validación estadística y la reproducibilidad (Park & Han, 2018; Varoquaux & Cheplygina, 2019).

OE2: Diseñar e implementar la arquitectura de persistencia. Crear una infraestructura que soporte el acceso concurrente de varios usuarios y la gestión del historial de diagnósticos y experimentos. Esta capa debe registrar los parámetros de cada inferencia, como la imagen, el modelo, la predicción, la confianza y los artefactos generados, y conservar la configuración, las métricas y los resultados de las sesiones de entrenamiento para poder consultarlos posteriormente.

OE3: Diseñar e implementar el control de acceso. Desarrollar un mecanismo de autenticación y autorización que mantenga separados los datos de cada usuario y proteja las operaciones de la plataforma. El objetivo incluye el registro, el inicio y el cierre de sesión, además de medidas frente a amenazas habituales de las aplicaciones web (OWASP, 2021), como la inyección, la falsificación de peticiones entre sitios y los intentos de acceso por fuerza bruta.

OE4: Implementar el pipeline de entrenamiento. Automatizar el entrenamiento y la evaluación de un conjunto amplio de arquitecturas de deep learning, tanto redes convolucionales como modelos basados en atención, mediante validación cruzada y particiones balanceadas. El pipeline debe incluir el preprocesamiento de las imágenes, la transferencia de conocimiento, el cálculo de métricas y el almacenamiento de los artefactos. Las diferencias de optimización entre familias deben quedar documentadas para que la comparación pueda interpretarse correctamente.

OE5: Desarrollar el módulo de explicabilidad (XAI). Implementar dos formas complementarias de analizar las decisiones del modelo. La primera generará mapas visuales para inspeccionar las zonas de la radiografía que influyen en cada predicción. La segunda calculará métricas sobre la fidelidad de esas explicaciones. Además, se evaluará la calibración para comprobar si la confianza del modelo se corresponde con su precisión.

OE6: Ejecutar la validación externa y el análisis estadístico. Evaluar los modelos sobre una cohorte independiente, sin reaprendizaje, para observar cómo responden ante una población, unos equipos y unos protocolos de imagen distintos. El análisis estadístico debe distinguir entre resultados descriptivos y contrastes inferenciales, tener en cuenta la dependencia entre pliegues y aplicar correcciones por comparaciones múltiples cuando corresponda (Park & Han, 2018; Nagendran & al., 2020; Nadeau & Bengio, 2003).

OE7: Favorecer la reproducibilidad y la trazabilidad de los experimentos. Fijar las semillas aleatorias, guardar la configuración de cada experimento y registrar los resultados y artefactos generados. Estas medidas permiten comprobar y repetir los resultados bajo las mismas condiciones, dentro de las limitaciones propias del hardware y del entorno de ejecución (Varoquaux & Cheplygina, 2019).

OE8: Desarrollar la interfaz clínica de diagnóstico asistido. Diseñar una interfaz web que permita cargar radiografías, obtener el diagnóstico y su confianza, consultar los mapas de explicabilidad y descargar un informe PDF desde un mismo panel. La interfaz debe estar dirigida a usuarios sin formación específica en inteligencia artificial y seguir las pautas de interacción humano-inteligencia artificial (Amershi & al., 2019).

OE9: Desarrollar el laboratorio MLOps y el asistente conversacional. Integrar un laboratorio de entrenamiento en la plataforma web con un asistente conversacional que ayude a configurar y lanzar experimentos sin escribir código. El sistema debe orquestar el pipeline descrito en los objetivos OE4, OE5 y OE6 y presentar sus resultados, comparativas e informes. La elección de este tipo de interfaz se apoya en trabajos que estudian el uso de agentes conversacionales en aplicaciones sanitarias (Laranjo & al., 2018; Tudor Car & al., 2020).

OE10: Diseñar e implementar el procesamiento asíncrono de tareas. Ejecutar los entrenamientos, los análisis de explicabilidad y las validaciones externas sin bloquear la interfaz. El sistema debe mostrar el estado y el progreso de cada tarea y permitir la cancelación de los trabajos pendientes cuando sea posible. Esta separación entre las peticiones web y los procesos largos también reduce parte de la complejidad operativa de los sistemas de aprendizaje automático (Sculley & al., 2015).

OE11: Incorporar internacionalización. Añadir soporte para que la interfaz, los informes y el asistente conversacional estén disponibles en español, inglés, chino e hindi. Con ello se amplía el uso de la plataforma a otros entornos lingüísticos.

En conjunto, estos objetivos cubren la revisión del problema, el diseño experimental, la construcción de la plataforma y sus mecanismos de evaluación. Cada uno se relaciona a lo largo de la memoria con los requisitos, casos de uso y componentes de diseño que le corresponden. La trazabilidad, la evidencia disponible y las limitaciones de su comprobación se resumen en el capítulo 33, sin confundir la verificación funcional de la plataforma con la interpretación de los resultados de los modelos. La administración avanzada de la plataforma queda fuera de este conjunto de objetivos y del alcance planificado del proyecto.

---

## Referencias del capítulo

Aggarwal, R., & al., e. (2021). Diagnostic accuracy of deep learning in medical imaging: A systematic review and meta-analysis. *NPJ Digital Medicine*, 4, 65.

Amershi, S., & al., e. (2019). Guidelines for human-AI interaction. *Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems*, 1-13.

De Fauw, J., & al., e. (2018). Clinically applicable deep learning for diagnosis and referral in retinal disease. *Nature Medicine*, 24, 1342-1350.

Esteva, A., & al., e. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*, 542, 115-118.

Kelly, C. J., & al., e. (2019). Key challenges for delivering clinical impact with artificial intelligence. *BMC Medicine*, 17, 195.

Kermany, D. S., & al., e. (2018). Identifying medical diagnoses and treatable diseases by image-based deep learning. *Cell*, 172(5), 1122-1131.e9. https://doi.org/10.1016/j.cell.2018.02.010

Tudor Car, L., Dhinagaran, D. A., Kyaw, B. M., Kowatsch, T., Joty, S., Theng, Y.-L., & Atun, R. (2020). Conversational agents in health care: Scoping review and conceptual analysis. *Journal of Medical Internet Research*, 22(8), e17158. https://doi.org/10.2196/17158

Laranjo, L., & al., e. (2018). Conversational agents in healthcare: A systematic review. *Journal of the American Medical Informatics Association*, 25(9), 1248-1258.

Liu, X., & al., e. (2019). A comparison of deep learning performance against health-care professionals in detecting diseases from medical imaging: A systematic review and meta-analysis. *The Lancet Digital Health*, 1(6), e271-e297.

McKinney, S. M., & al., e. (2020). International evaluation of an AI system for breast cancer screening. *Nature*, 577, 89-94.

Nadeau, C., & Bengio, Y. (2003). Inference for the generalization error. *Machine Learning*, 52, 239-281. https://doi.org/10.1023/A:1024068626366

Nagendran, M., Chen, Y., Lovejoy, C. A., Gordon, A. C., Komorowski, M., Harvey, H., Topol, E. J., Ioannidis, J. P. A., Collins, G. S., & Maruthappu, M. (2020). Artificial intelligence versus clinicians: Systematic review of design, reporting standards, and claims of deep learning studies. *BMJ*, 368, m689. https://doi.org/10.1136/bmj.m689

OWASP. (2021). *OWASP Top 10:2021 – The ten most critical web application security risks*. Obtenido de https://owasp.org/Top10/

Park, S. H., & Han, K. (2018). Methodologic guide for evaluating clinical performance and effect of artificial intelligence technology for medical diagnosis and prediction. *Radiology*, 286(3), 800-809.

Sculley, D., & al., e. (2015). Hidden technical debt in machine learning systems. *Advances in Neural Information Processing Systems*, 28, 2503-2511.

Varoquaux, G., & Cheplygina, V. (2019). Machine learning for medical imaging: Methodological failures and recommendations for the future. *NPJ Digital Medicine*, 2, 48.
