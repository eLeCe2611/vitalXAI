# Project — vitalXAI

Datos del plan de proyecto (sprints, tareas, recursos, horas, costes y fechas) tal y como quedan configurados en Microsoft Project.

## Reparto de recursos

| Recurso | Horas | Coste | Inicio | Fin |
|---|---|---|---|---|
| Luis Carmona Berdugo | 455,14 h | 9.102,80 € | lun 24/11/25 | mié 02/09/26 |
| Aurelio López Fernández | 9,5 h | 475,00 € | lun 24/11/25 | mar 01/09/26 |
| Vicente de Vides Rodríguez | 1,5 h | 75,00 € | lun 02/03/26 | mar 03/03/26 |
| Iván Segura Carmona | 5,96 h | 298,00 € | mié 01/04/26 | jue 18/06/26 |
| Marc Ríos Cadena | 1,9 h | 95,00 € | vie 10/04/26 | jue 18/06/26 |

## Diagrama de Gantt

| Nivel | Nombre | Duración | Inicio | Fin | Recursos | Horas |
|---|---|---|---|---|---|---|
| 0 | VitalXAI | 203 días | lun 24/11/25 | mié 02/09/26 | | 474 h |
| 1 | 0. Planificación del Proyecto | 70 días | lun 24/11/25 | vie 27/02/26 | | 42 h |
| 2 | 0.1 Reunión inicial | 1 día | lun 24/11/25 | lun 24/11/25 | Luis Carmona Berdugo[50%];Aurelio López Fernández[50%] | 3 h |
| 2 | 0.2 Redacción del Plan de Proyecto | 49 días | mar 25/11/25 | vie 30/01/26 | Luis Carmona Berdugo | 25 h |
| 2 | 0.3 Inicialización del marco tecnológico | 10 días | lun 02/02/26 | vie 13/02/26 | Luis Carmona Berdugo | 8 h |
| 2 | 0.4 Cronograma en Microsoft Project | 10 días | lun 16/02/26 | vie 27/02/26 | Luis Carmona Berdugo | 6 h |
| 1 | 1. Infraestructura y Seguridad | 12 días | lun 02/03/26 | mar 17/03/26 | | 70 h |
| 2 | 1.1 Diseño del modelo de datos en MySQL | 2 días | lun 02/03/26 | mar 03/03/26 | Luis Carmona Berdugo[85%];Vicente de Vides Rodríguez[15%] | 10 h |
| 2 | 1.2 Backend FastAPI y conexión a la BD | 2 días | mié 04/03/26 | jue 05/03/26 | Luis Carmona Berdugo | 14 h |
| 2 | 1.3 Registro, login y cierre de sesión | 2 días | vie 06/03/26 | lun 09/03/26 | Luis Carmona Berdugo | 12 h |
| 2 | 1.4 Pantallas de autenticación | 2 días | lun 09/03/26 | mar 10/03/26 | Luis Carmona Berdugo | 8 h |
| 2 | 1.5 Hashing de contraseñas y tokens de sesión | 3 días | mar 10/03/26 | jue 12/03/26 | Luis Carmona Berdugo | 6 h |
| 2 | 1.6 Protección CSRF y limitación de peticiones | 2 días | mié 11/03/26 | vie 13/03/26 | Luis Carmona Berdugo | 6 h |
| 2 | 1.7 Pruebas de compatibilidad de librerías y entorno | 2 días | jue 12/03/26 | lun 16/03/26 | Luis Carmona Berdugo | 6 h |
| 2 | 1.8 Pruebas de seguridad e inyección SQL | 2 días | lun 16/03/26 | mar 17/03/26 | Luis Carmona Berdugo | 8 h |
| 1 | 2. Motor de diagnóstico | 10 días | mié 18/03/26 | mar 31/03/26 | | 41 h |
| 2 | 2.1 Carga y caché de modelos preentrenados | 3 días | mié 18/03/26 | vie 20/03/26 | Luis Carmona Berdugo | 15 h |
| 2 | 2.2 Predicción y pantalla de disgnóstico | 3 días | lun 23/03/26 | mié 25/03/26 | Luis Carmona Berdugo | 18 h |
| 2 | 2.3 Informe PDF del diagnóstico | 4 días | jue 26/03/26 | mar 31/03/26 | Luis Carmona Berdugo | 8 h |
| 1 | 3. Explicabilidad | 8 días | mié 01/04/26 | vie 10/04/26 | | 48 h |
| 2 | 3.1 Saliency Maps | 2 días | mié 01/04/26 | jue 02/04/26 | Luis Carmona Berdugo[90%];Iván Segura Carmona[10%] | 10 h |
| 2 | 3.2 SmoothGrad | 1 día | vie 03/04/26 | vie 03/04/26 | Luis Carmona Berdugo | 8 h |
| 2 | 3.3 Grad-CAM | 2 días | lun 06/04/26 | mar 07/04/26 | Iván Segura Carmona[8%];Luis Carmona Berdugo[92%] | 12 h |
| 2 | 3.4 Mapas de atención | 1 día | mié 08/04/26 | mié 08/04/26 | Luis Carmona Berdugo | 8 h |
| 2 | 3.5 Integración de las explicaciones en el diagnóstico | 1 día | jue 09/04/26 | jue 09/04/26 | Luis Carmona Berdugo | 6 h |
| 2 | 3.6 Revisión de coherencia clínica con asesor | 1 día | vie 10/04/26 | vie 10/04/26 | Luis Carmona Berdugo[75%];Marc Ríos Cadena[25%] | 4 h |
| 1 | 4. Entrenamiento CNN | 10 días | lun 13/04/26 | vie 24/04/26 | | 52 h |
| 2 | 4.1 Script de entrenamiento con validación cruzada | 4 días | lun 13/04/26 | jue 16/04/26 | Iván Segura Carmona[3%];Luis Carmona Berdugo[97%] | 20 h |
| 2 | 4.2 Ajuste de hiperparámetros y primeras ejecuciones | 2 días | vie 17/04/26 | lun 20/04/26 | Luis Carmona Berdugo | 14 h |
| 2 | 4.3 Integración del entrenamiento en el backend | 1 día | mar 21/04/26 | mar 21/04/26 | Luis Carmona Berdugo | 8 h |
| 2 | 4.4 Panel de monitorización del progreso | 3 días | mié 22/04/26 | vie 24/04/26 | Luis Carmona Berdugo | 10 h |
| 1 | 5. Transformers y análisis XAI | 17 días | lun 27/04/26 | mar 19/05/26 | | 62 h |
| 2 | 5.1 Script de entrenamiento de arquitecturas Transformer | 3 días | lun 27/04/26 | mié 29/04/26 | Iván Segura Carmona[3%];Luis Carmona Berdugo[97%] | 16 h |
| 2 | 5.2 Script de explicabilidad cualitativa | 3 días | jue 30/04/26 | lun 04/05/26 | Luis Carmona Berdugo | 10 h |
| 2 | 5.3 Script de métricas cuantitativas y calibración | 3 días | lun 04/05/26 | mié 06/05/26 | Iván Segura Carmona[8%];Luis Carmona Berdugo[92%] | 12 h |
| 2 | 5.4 Orquestación automática post-entreno | 1 día | jue 07/05/26 | vie 08/05/26 | Luis Carmona Berdugo | 6 h |
| 2 | 5.5 Entrenamiento de Deit, Swin y ViT | 5 días | lun 11/05/26 | vie 15/05/26 | Luis Carmona Berdugo | 14 h |
| 2 | 5.6 Revisión de resultados con el asesor de deep learning | 7 días | lun 18/05/26 | mar 26/05/26 | Iván Segura Carmona[25%];Luis Carmona Berdugo[75%] | 4 h |
| 1 | 6. Validación externa | 4 días | mar 19/05/26 | vie 22/05/26 | | 26 h |
| 2 | 6.1 Comparación estadística: ranking y test de Wilcoxon | 2 días | mar 19/05/26 | mié 20/05/26 | Iván Segura Carmona[8%];Luis Carmona Berdugo[92%] | 12 h |
| 2 | 6.2 Validación externa y test de DeLong | 2 días | jue 21/05/26 | vie 22/05/26 | Luis Carmona Berdugo | 14 h |
| 1 | 7. Laboratorio MLOps | 10 días | lun 25/05/26 | vie 05/06/26 | | 66 h |
| 2 | 7.1 Integración de la API de Groq | 1 día | lun 25/05/26 | lun 25/05/26 | Luis Carmona Berdugo | 8 h |
| 2 | 7.2 Diseño del prompt del asistente | 2 días | mar 26/05/26 | mié 27/05/26 | Luis Carmona Berdugo | 12 h |
| 2 | 7.3 Asistente conversacional del laboratorio | 2 días | jue 28/05/26 | vie 29/05/26 | Luis Carmona Berdugo | 14 h |
| 2 | 7.4 Lanzamiento de experimentos desde el chat | 1 día | lun 01/06/26 | lun 01/06/26 | Luis Carmona Berdugo | 8 h |
| 2 | 7.5 Cola de trabajos y ejecución asíncrona | 1 día | mar 02/06/26 | mar 02/06/26 | Luis Carmona Berdugo | 8 h |
| 2 | 7.6 Internacionalización de la plataforma | 1 día | mié 03/06/26 | mié 03/06/26 | Luis Carmona Berdugo | 8 h |
| 2 | 7.7 Vistas de resultados, rankings y curvas ROC | 1 día | jue 04/06/26 | jue 04/06/26 | Luis Carmona Berdugo | 8 h |
| 1 | 8. Documentación y cierre | 64 días | vie 05/06/26 | mié 02/09/26 | | 67 h |
| 2 | 8.1 Benchmarking final con todas las arqitecturas | 10 días | vie 05/06/26 | jue 18/06/26 | Iván Segura Carmona[5%];Luis Carmona Berdugo[90%];Marc Ríos Cadena[5%] | 18 h |
| 2 | 8.2 Redacción de la memoria y manuales | 50 días | vie 19/06/26 | jue 27/08/26 | Luis Carmona Berdugo | 30 h |
| 2 | 8.3 Reunión final y correcciones | 3 días | vie 28/08/26 | mar 01/09/26 | Aurelio López Fernández[50%];Luis Carmona Berdugo[50%] | 16 h |
| 2 | 8.4 Entrega final | 1 día | mié 02/09/26 | mié 02/09/26 | Luis Carmona Berdugo | 3 h |
