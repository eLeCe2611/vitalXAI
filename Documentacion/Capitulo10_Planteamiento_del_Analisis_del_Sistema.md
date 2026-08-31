# Capítulo 10: Planteamiento del análisis del sistema

Para diseñar e implementar un sistema es necesario concretar la idea inicial en afirmaciones verificables sobre sus capacidades, sus restricciones y sus usuarios. Esta parte de la memoria desarrolla esa concreción y este capítulo introduce el propósito y las dimensiones del análisis (Larman, 2004; Wiegers & Beatty, 2013).

## 10.1 Propósito del análisis

El análisis fija las bases sobre las que se construirá el sistema. Por un lado, evita asumir durante el diseño y la implementación capacidades que no forman parte del alcance o dejar fuera requisitos acordados. Por otro, documenta las restricciones del entorno y las decisiones de alcance, de modo que el tutor, el tribunal o un futuro mantenedor puedan entender qué debe ofrecer el sistema y cuáles son sus límites.

En este proyecto, la formalización del análisis es especialmente relevante porque el sistema combina una aplicación web orientada al diagnóstico asistido y un laboratorio de investigación de aprendizaje automático. La primera requiere claridad, seguridad y facilidad de uso; el segundo requiere flexibilidad, reproducibilidad y capacidad para ejecutar experimentos. El análisis permite considerar ambas perspectivas desde el inicio y dejar documentadas las decisiones que afectan a cada una.

## 10.2 Dimensiones del análisis

El análisis del sistema comienza con la definición de sus objetivos y de su ámbito. El capítulo 11 delimita las capacidades de la plataforma, el entorno tecnológico, la normativa aplicable y los perfiles de usuario. Estos elementos establecen el contexto del producto, pero no agotan el análisis. A partir de ellos, los capítulos siguientes transforman las necesidades del proyecto en requisitos verificables, casos de uso, subsistemas, entidades del dominio y pruebas de consistencia y comportamiento.

Sobre esa base, el análisis especifica qué debe hacer el sistema y cómo se organiza para ofrecer esas capacidades. Esta parte se estructura en los capítulos 12 a 16:

- **Especificación de requisitos y casos de uso (capítulo 12).** Se definen los requisitos funcionales y no funcionales del sistema y los casos de uso que describen la interacción de cada perfil de usuario con la plataforma.
- **Identificación de subsistemas (capítulo 13).** Las capacidades del sistema se agrupan en subsistemas de análisis, lo que permite organizar el resto del análisis y, posteriormente, el diseño.
- **Modelo de dominio (capítulo 14).** Se identifican las entidades que el sistema debe gestionar y se describe su comportamiento dinámico mediante secuencias de interacción.
- **Verificación de la consistencia (capítulo 15).** Se comprueba la coherencia entre los objetivos, los requisitos, los casos de uso y los subsistemas.
- **Plan de pruebas (capítulo 16).** Se define la estrategia de pruebas que verificará el cumplimiento de lo especificado.

El conjunto de estas dimensiones constituye el marco de referencia del diseño del sistema, desarrollado en la parte siguiente de la memoria.
