# Capítulo 10: Planteamiento del análisis del sistema

Para que un sistema se diseñe e implemente con garantías no basta con una idea general: es necesario formalizar el análisis, es decir, convertir la visión del proyecto en un conjunto de afirmaciones verificables sobre qué debe hacer el sistema, bajo qué restricciones y para qué usuarios. Esta parte de la memoria se ocupa precisamente de eso, y este capítulo abre el análisis presentando su propósito y sus dimensiones.

## 10.1 Propósito del análisis

El documento de análisis fija de manera explícita y sin ambigüedades las bases sobre las que se construirá el sistema. Su utilidad es doble. Por un lado, evita que durante el diseño y la implementación se asuman capacidades que no se planificaron o se omitan requisitos que sí se acordaron. Por otro lado, documenta las decisiones de alcance y las restricciones del entorno, de modo que cualquier lector —el tutor, el tribunal o un futuro mantenedor— pueda entender por qué el sistema tiene la forma que tiene y cuáles de sus límites son deliberados y cuáles responden a restricciones técnicas.

En este proyecto, la formalización del análisis es especialmente relevante porque el sistema aúna dos naturalezas: una aplicación web de uso clínico y un laboratorio de investigación de aprendizaje automático. La primera impone requisitos de claridad, seguridad y facilidad de uso; la segunda impone requisitos de flexibilidad, reproducibilidad y capacidad de ejecutar experimentos completos. Formalizar el análisis permite reconciliar ambas perspectivas desde el inicio y evitar que una de las dos naturalezas acabe imponiéndose sobre la otra sin que esa decisión quede documentada.

## 10.2 Dimensiones del análisis

El análisis del sistema comprende, en primer lugar, la delimitación del contexto en el que se inscribe la plataforma. Esta delimitación se apoya en cuatro dimensiones: el alcance funcional del sistema, que fija qué capacidades se compromete a entregar y cuáles quedan deliberadamente fuera de su ámbito de responsabilidad; el entorno tecnológico, que describe el ecosistema sobre el que se construye la plataforma y las restricciones que impone al diseño; la normativa y los estándares que el sistema debe observar; y la caracterización de los perfiles de usuario que interactuarán con él, atendiendo a sus conocimientos, sus necesidades y su nivel de acceso. Estas cuatro dimensiones, junto con los objetivos del sistema que las enmarcan, se desarrollan íntegramente en el capítulo 11.

Sobre esa base, el análisis especifica qué debe hacer el sistema y cómo se organiza internamente para lograrlo, y es esta segunda parte la que constituye el grueso del análisis. Se estructura en los capítulos 12 a 16:

- **Especificación de requisitos y casos de uso (capítulo 12).** Se definen los requisitos funcionales y no funcionales del sistema y los casos de uso que describen la interacción de cada perfil de usuario con la plataforma.
- **Identificación de subsistemas (capítulo 13).** Las capacidades del sistema se agrupan en subsistemas de análisis, lo que permite organizar el resto del análisis y, posteriormente, el diseño.
- **Modelo de dominio (capítulo 14).** Se identifican las entidades que el sistema debe gestionar y se describe su comportamiento dinámico mediante secuencias de interacción.
- **Verificación de la consistencia (capítulo 15).** Se comprueba la coherencia entre los objetivos, los requisitos, los casos de uso y los subsistemas.
- **Plan de pruebas (capítulo 16).** Se define la estrategia de pruebas que verificará el cumplimiento de lo especificado.

El conjunto de estas dimensiones constituye el contrato sobre el que se sustenta el diseño del sistema, desarrollado en la parte siguiente de la memoria.
