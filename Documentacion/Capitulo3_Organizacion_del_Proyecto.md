# Capítulo 3: Estructura organizativa y partes interesadas del proyecto

Este capítulo describe la estructura organizativa del proyecto y las personas e instituciones relacionadas con su desarrollo. Al tratarse de un trabajo unipersonal y multidisciplinar, es necesario distinguir quién participa, qué función desempeña y qué tipo de relación mantiene con el alumno desarrollador. El capítulo se divide en tres apartados. El apartado 3.1 presenta el organigrama y las relaciones entre las partes interesadas. El apartado 3.2 identifica esos perfiles y resume su papel general. El apartado 3.3 detalla sus responsabilidades y presenta la matriz RACI para las principales fases y entregables.

## 3.1 Estructura organizativa del proyecto

El organigrama representa las relaciones entre las partes interesadas del proyecto. Incluye nueve nodos: Marc Ríos Cadenas, Iván Segura Carmona, Aurelio López Fernández, Luis Carmona Berdugo, el consultor de persistencia y bases de datos Vicente de Vides Rodríguez, Rubén Pérez Garrido, el Tribunal de Evaluación del TFG, el Laboratorio Synergia y los facultativos e investigadores clínicos. Estos dos últimos representan a los usuarios objetivo de la plataforma y no mantienen una relación jerárquica con los integrantes del equipo.

```mermaid
graph TB
    subgraph Direccion["Dirección Académica"]
        ALF[Aurelio López Fernández<br/><b>Tutor Académico</b>]
    end

    subgraph Equipo["Equipo de Desarrollo"]
        LCB[Luis Carmona Berdugo<br/><b>Alumno Desarrollador</b>]
    end

    subgraph Asesoria["Asesoría y Consultoría"]
        ISC[Iván Segura Carmona<br/>Asesor de Deep Learning y XAI]
        MRC[Marc Ríos Cadenas<br/>Asesor de Imagen Médica]
        VVR[Vicente de Vides Rodríguez<br/>Consultor de Persistencia y Bases de Datos]
        RPG[Rubén Pérez Garrido<br/>Asesor de Ingeniería del Software y Metodología]
    end

    subgraph Evaluacion["Evaluación"]
        TTFG[Tribunal de Evaluación del TFG]
    end

    subgraph Usuarios["Usuarios objetivo"]
        LS[Laboratorio Synergia]
        FIC[Facultativos e<br/>Investigadores Clínicos]
    end

    ALF -->|Tutoriza| LCB
    LCB -->|Consulta| ISC
    LCB -->|Consulta| MRC
    LCB -->|Consulta| VVR
    LCB -->|Consulta| RPG
    ALF -.->|Informa| TTFG
    TTFG -->|Evalúa| LCB
    LS -.->|Usuario objetivo| LCB
    FIC -.->|Usuarios objetivo| LCB

    style LCB fill:#2563EB,color:#fff,stroke:#1E40AF
    style ALF fill:#16A34A,color:#fff,stroke:#166534
    style TTFG fill:#DC2626,color:#fff,stroke:#991B1B
    style ISC fill:#EA580C,color:#fff,stroke:#9A3412
    style MRC fill:#EA580C,color:#fff,stroke:#9A3412
    style VVR fill:#EA580C,color:#fff,stroke:#9A3412
    style RPG fill:#EA580C,color:#fff,stroke:#9A3412
    style LS fill:#7C3AED,color:#fff,stroke:#5B21B6
    style FIC fill:#7C3AED,color:#fff,stroke:#5B21B6
```

*Figura 1 - Organigrama del proyecto*

## 3.2 Partes interesadas del proyecto

La identificación de las partes interesadas permite distinguir quién se ve afectado por el proyecto, quién aporta conocimiento y quién participa en la revisión del resultado. En este caso conviven el alumno desarrollador, el tutor, varios asesores, el tribunal y los colectivos que representan a los usuarios objetivo. A continuación se resume el papel general de cada uno:

- **Luis Carmona Berdugo (Alumno Desarrollador)**: Asume la responsabilidad principal de la ejecución técnica y documental. Diseña, implementa, prueba y documenta el sistema, y coordina la comunicación con el tutor y los asesores.
- **Aurelio López Fernández (Tutor Académico)**: Supervisa el desarrollo académico del trabajo, revisa las entregas y orienta sobre su alcance, metodología y presentación.
- **Tribunal de Evaluación del TFG (Evaluador)**: Examina la memoria, el sistema y la defensa oral conforme a los criterios académicos de la universidad, y determina la calificación final.
- **Vicente de Vides Rodríguez (Consultor de Persistencia y Bases de Datos)**: Aporta asesoramiento puntual sobre el diseño, el modelado y la persistencia de los datos. La decisión final y la implementación corresponden al alumno.
- **Iván Segura Carmona (Asesor de Deep Learning y XAI)**: Aporta asesoramiento sobre las arquitecturas de aprendizaje profundo, las técnicas de explicabilidad y la interpretación de los resultados experimentales.
- **Marc Ríos Cadenas (Asesor de Imagen Médica)**: Aporta contexto sobre la interpretación de radiografías y sobre el uso previsto de la plataforma en un entorno clínico, sin participar en la implementación.
- **Rubén Pérez Garrido (Asesor de Ingeniería del Software y Metodología)**: Es consultado puntualmente sobre la metodología de desarrollo, las prácticas de ingeniería y la calidad del proceso.
- **Laboratorio Synergia (Parte interesada / Usuario objetivo)**: Representa un posible entorno de adopción cuyas líneas de investigación son afines a los objetivos de vitalXAI. En el proyecto no se realizaron sesiones de uso ni evaluaciones con este laboratorio.
- **Facultativos e investigadores clínicos (Usuarios objetivo)**: Constituyen el colectivo al que se dirige el sistema. Sus necesidades se utilizan como referencia para definir el alcance y las funcionalidades, pero no se realizó una evaluación empírica con usuarios reales durante el proyecto.

## 3.3 Responsabilidades, funciones y participación de las partes interesadas

La definición de responsabilidades ayuda a ordenar el trabajo y a distinguir quién ejecuta, quién aprueba y quién aporta asesoramiento. Esta distinción es especialmente útil en un proyecto multidisciplinar, porque las partes interesadas intervienen en fases diferentes y con niveles de participación distintos.

**Alumno Desarrollador (Luis Carmona Berdugo, LCB)**: Ejecuta el proyecto y asume la responsabilidad de sus decisiones técnicas y documentales. Revisa el estado del arte, diseña la arquitectura, implementa los módulos y pipelines, prepara las pruebas, analiza los resultados disponibles y redacta la memoria y el manual de usuario. También mantiene la planificación, gestiona los riesgos y coordina la comunicación con el tutor y los asesores. La validez y el alcance de los resultados deben interpretarse según las condiciones experimentales y las limitaciones documentadas en la memoria.

**Tutor Académico (Aurelio López Fernández, ALF)**: Revisa las entregas y proporciona retroalimentación sobre el rigor académico, la coherencia del trabajo y su adecuación a los objetivos del TFG. Orienta al alumno en las decisiones de alcance y presentación, pero la ejecución y las decisiones finales del proyecto corresponden al alumno desarrollador.

**Tribunal de Evaluación del TFG (T. TFG)**: Evalúa la memoria, el sistema y la defensa oral según los criterios académicos establecidos por la universidad. No participa directamente en el desarrollo y su intervención se produce en la evaluación final. La claridad de la exposición, la justificación de las decisiones y la delimitación de las conclusiones forman parte de los aspectos que debe valorar.

**Consultor de Persistencia y Bases de Datos (Vicente de Vides Rodríguez, VVR)**: Su intervención se concentra en la tarea 1.1 y tiene carácter consultivo. Aporta criterios sobre el diseño, el modelado y la optimización del esquema de datos, mientras que la decisión definitiva y la implementación corresponden al alumno desarrollador.

**Asesor de Deep Learning y XAI (Iván Segura Carmona, ISC)**: Participa con carácter consultivo en la revisión de las arquitecturas, las técnicas de explicabilidad, las métricas y los resultados del benchmarking. El alumno conserva la responsabilidad de diseñar, implementar, ejecutar y documentar estas partes del proyecto.

**Asesor de Imagen Médica (Marc Ríos Cadenas, MRC)**: Participa de forma consultiva en la revisión del contexto médico y radiológico, especialmente en la interpretación de radiografías y de los mapas de explicabilidad. Sus observaciones sirven como referencia de dominio; la traducción de esas observaciones a requisitos, diseño e implementación corresponde al alumno.

**Asesor de Ingeniería del Software y Metodología (Rubén Pérez Garrido, RPG)**: Su participación es puntual y consultiva. Aporta criterios sobre la aplicación de la metodología, las prácticas de desarrollo guiado por pruebas y la calidad del proceso de ingeniería en las tareas de implementación. La ejecución concreta de dichas tareas y la aplicación de la metodología son responsabilidad del alumno.

**Laboratorio Synergia y Facultativos e investigadores clínicos (LS/FIC)**: Mantienen una posición externa al núcleo de programación y representan a los usuarios objetivo del sistema. No participaron en el desarrollo ni realizaron sesiones de uso o evaluaciones de usabilidad. Por tanto, sus necesidades se consideran una referencia de diseño, no una medida empírica de la utilidad de la plataforma. La usabilidad se aborda mediante los requisitos y las decisiones de interfaz, pero queda como una limitación del proyecto la ausencia de una evaluación con usuarios reales.

La matriz RACI se utiliza en este proyecto para resumir la participación de cada interesado en las fases y entregables principales. Sus letras representan Responsible, quien ejecuta el trabajo; Accountable, quien asume la aprobación final; Consulted, quien aporta conocimiento; e Informed, quien recibe información sobre el avance o el resultado.

En esta aplicación, R identifica al alumno como responsable de ejecutar la tarea y A al tutor como responsable de su supervisión académica, salvo en la defensa final, cuya evaluación corresponde al tribunal. Los asesores y el consultor aparecen como C cuando su conocimiento puede orientar una decisión, mientras que I indica que el interesado solo recibe información. Un guion representa que no se ha asignado participación en esa fase o entregable.

A continuación, se presenta la matriz RACI del proyecto, en la que las filas recogen las principales fases y entregables del ciclo de vida del proyecto, y las columnas representan los interesados identificados en el apartado anterior.

| Fase / Entregable | LCB | ALF | T. TFG | Consultor BD | ISC | MRC | RPG | LS/FIC |
|---|---|---|---|---|---|---|---|---|
| Revisión del estado del arte | R | A | I | - | C | C | - | - |
| Diseño de la arquitectura del sistema | R | A | I | C | - | - | - | - |
| Diseño e implementación de la base de datos | R | A | I | C | - | - | - | - |
| Implementación del pipeline de entrenamiento CNN y Transformer | R | A | I | - | C | - | C | - |
| Implementación del módulo XAI (cualitativo y cuantitativo) | R | A | I | - | C | C | C | - |
| Desarrollo de la interfaz web y chatbot conversacional | R | A | I | - | - | - | C | - |
| Seguridad y control de acceso | R | A | I | - | - | - | C | - |
| Pruebas y verificación del sistema | R | A | I | - | C | C | C | - |
| Laboratorio MLOps | R | A | I | - | C | - | C | - |
| Procesamiento asíncrono de tareas | R | A | I | - | - | - | C | - |
| Internacionalización de la plataforma | R | A | I | - | - | - | C | - |
| Panel de administración | R | A | I | - | - | - | C | - |
| Gestión de riesgos | R | A | I | - | - | - | C | - |
| Benchmarking y análisis de resultados | R | A | I | - | C | C | - | - |
| Validación del contexto clínico | R | A | I | - | - | C | - | - |
| Validación externa y tests estadísticos | R | A | I | - | C | - | - | - |
| Documentación del TFG | R | A | I | - | - | - | I | - |
| Defensa y evaluación final | R | C | A | - | - | - | - | - |

*Tabla 1 - Matriz RACI del proyecto*
