# Capítulo 31: Codificación del laboratorio MLOps

El laboratorio MLOps constituye el segundo núcleo funcional de vitalXAI: permite configurar, lanzar y analizar experimentos de entrenamiento de modelos de detección de neumonía, con validación cruzada, análisis de explicabilidad, comparación estadística y validación externa sobre cohortes independientes. El término MLOps se utiliza aquí para referirse a la coordinación del ciclo de entrenamiento, evaluación y gestión de resultados (Kreuzberger, Kühl, & Hirschl, 2023). Este capítulo describe su implementación, principalmente en `mlops_engine.py`, que organiza las sesiones y orquesta el pipeline, y en `pdf_generator_mlops.py`, que genera el informe consolidado de cada sesión. El contenido se organiza en seis apartados: metodología experimental, orquestación del entrenamiento, validación externa y comparación estadística, gestión de sesiones, lectura de resultados y generación del informe.

La codificación del laboratorio sigue la decisión de diseño del capítulo 23: el pipeline de experimentación se ejecuta mediante los scripts del directorio `pneumoniacnn-main/code`, que el motor invoca como procesos externos con la configuración de cada trabajo transmitida por variables de entorno. Los scripts realizan el entrenamiento con validación cruzada, el análisis XAI cualitativo y cuantitativo, la comparación estadística y la validación externa, y escriben sus resultados en el directorio `training_results` de la sesión. El motor orquesta la ejecución de los scripts y resuelve la lectura de los resultados, manteniendo la persistencia híbrida de la plataforma: la cola y el estado en MySQL, y los artefactos en el sistema de ficheros.

El código completo del laboratorio y de los scripts experimentales puede consultarse en [github.com/eLeCe2611/vitalXAI](https://github.com/eLeCe2611/vitalXAI), en `services/mlops_engine.py`, `services/trainer_engine.py`, `services/pdf_generator_mlops.py` y `pneumoniacnn-main/code/`. Los fragmentos incluidos aquí se limitan a las decisiones necesarias para comprender la ejecución del pipeline y la lectura de sus resultados.

## 31.1 Metodología experimental del pipeline

El pipeline se ha diseñado para comparar diecinueve arquitecturas, dieciséis convolucionales y tres basadas en Transformers, bajo un procedimiento común. La evaluación utiliza cinco pliegues estratificados: en cada iteración se entrena con cuatro pliegues y se valida con el restante, de forma que cada imagen participa una vez en la validación. El resultado de cada arquitectura se resume mediante la media y la desviación típica de las métricas obtenidas en los cinco pliegues.

El conjunto de entrenamiento presenta un mayor número de imágenes de neumonía que de imágenes normales. Para evitar que esta diferencia determine por sí sola el aprendizaje, el pipeline aplica submuestreo aleatorio de la clase mayoritaria dentro de cada partición de entrenamiento. La validación conserva la distribución completa de cada pliegue. Esta decisión facilita la comparación entre modelos, aunque implica descartar parte de las imágenes disponibles y limita las conclusiones frente a otras estrategias de balanceo que no se han comparado en un experimento independiente (He & Garcia, 2009).

Las CNN utilizan pesos preentrenados en ImageNet, mantienen congelada la base convolucional y actualizan un cabezal de clasificación binaria. Los Transformers parten de pesos preentrenados y ajustan el modelo completo con una tasa de aprendizaje menor y `AdamW` (Loshchilov & Hutter, 2019). En ambas familias se aplican transformaciones ligeras de las imágenes y se guarda el mejor modelo de cada pliegue según la pérdida de validación. También se utilizan parada temprana, reducción de la tasa de aprendizaje cuando el aprendizaje se estanca y la semilla global 42. En las CNN, mantener congelada la base reduce los parámetros que se ajustan con las radiografías, aunque puede limitar la adaptación de las características al dominio médico (Deng & al., 2009; Yosinski & al., 2014).

El rendimiento se resume mediante exactitud, precisión, sensibilidad, F1 y AUC. El pipeline conserva las métricas de cada pliegue, su media y su desviación típica, junto con las predicciones y los pesos del mejor modelo. La curva ROC y su AUC permiten valorar la discriminación sin limitarse a un único umbral (Fawcett, 2006). La evaluación de las explicaciones añade Deletion AUC, Insertion AUC, Sparsity, Entropy y Stability SSIM, además del Brier Score y el Expected Calibration Error para valorar la calibración. En el script cuantitativo, estas dos últimas métricas se calculan sobre una muestra de diez imágenes, cinco por clase, por lo que no deben interpretarse como una evaluación clínica general de la calibración (Linardatos, Papastefanopoulos, & Kotsiantis, 2021; Guo, Pleiss, Sun, & Weinberger, 2017).

La comparación entre modelos mediante Wilcoxon se mantiene como análisis exploratorio sobre las AUC de los pliegues (Wilcoxon, 1945). Con cinco pares dependientes, el p-valor bilateral mínimo es 0,0625 y los pliegues no son observaciones independientes; por tanto, la matriz no permite afirmar significación estadística con el umbral habitual de 0,05 (Nadeau & Bengio, 2003). El ranking ordena las arquitecturas por AUC media y la matriz se conserva como apoyo descriptivo, sin una figura que sugiera conclusiones confirmatorias. La validación externa utiliza modelos congelados sobre la cohorte adulta independiente y emplea DeLong para comparar sus curvas ROC (DeLong, DeLong, & Clarke-Pearson, 1988), teniendo en cuenta que este resultado también debe interpretarse junto con las limitaciones del cambio de población y de las fuentes de las imágenes (Varma & Simon, 2006).

## 31.2 Orquestación del pipeline de entrenamiento

La orquestación del entrenamiento se implementa en la función `run_training_queue`, que coordina las etapas de una sesión: por cada modelo configurado, lanza el script de entrenamiento adecuado, convolucional o Transformer, y los scripts de análisis XAI; al finalizar ejecuta el script de comparación estadística. La configuración de cada trabajo se transmite a los scripts mediante variables de entorno, y el registro de la ejecución se escribe en el archivo de log del entrenamiento. El fragmento siguiente muestra la implementación del bucle de orquestación.

```python
def run_training_queue(session_id, models, dataset_path, epochs, batch_size, learning_rate):
    base_path = os.getcwd()
    script_train_cnn = os.path.join(base_path, "pneumoniacnn-main", "code", "1_train_kfold.py")
    script_train_trans = os.path.join(base_path, "pneumoniacnn-main", "code", "2_train_transformer_kfold.py")
    script_img = os.path.join(base_path, "pneumoniacnn-main", "code", "6_xai_qualitative.py")
    script_math = os.path.join(base_path, "pneumoniacnn-main", "code", "7_xai_quantitative.py")

    for model_name in models:
        env_vars = os.environ.copy()
        env_vars.update({
            "TFG_SESSION_ID": session_id, "TFG_MODEL_NAME": model_name,
            "TFG_DATASET_DIR": dataset_path, "TFG_EPOCHS": str(epochs),
            "TFG_BATCH_SIZE": str(batch_size), "TFG_LEARNING_RATE": str(learning_rate),
        })
        is_trans = model_name in TRANSFORMER_MODELS
        script_to_run = script_train_trans if is_trans else script_train_cnn
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
            subprocess.Popen(["python", script_to_run], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
            subprocess.Popen(["python", script_img], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
            subprocess.Popen(["python", script_math], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()

    env_vars_comp = os.environ.copy()
    env_vars_comp["TFG_SESSION_ID"] = session_id
    script_comp = os.path.join(base_path, "pneumoniacnn-main", "code", "3_evaluate_statistics.py")
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        subprocess.Popen(["python", script_comp], stdout=log, stderr=subprocess.STDOUT, env=env_vars_comp, text=True, encoding="utf-8", errors="replace").wait()
```

*Código 31.1 - Orquestación del pipeline de entrenamiento (`services/mlops_engine.py`)*

La implementación de la orquestación refleja la decisión de delegar la computación intensiva en los scripts del pipeline. El motor itera sobre los modelos de la sesión, transmite la configuración mediante las variables de entorno `TFG_*` y ejecuta el script de entrenamiento correspondiente, el script 1 para las CNN o el script 2 para las Transformer, seguido de los scripts de análisis XAI cualitativo y cuantitativo. La salida de los scripts se dirige al archivo de registro, de modo que la consola del laboratorio refleja la progresión del entrenamiento. Al completar todos los modelos, se ejecuta el script de comparación estadística, que genera el ranking y la matriz de Wilcoxon. Este flujo se ejecuta en el worker de la cola descrito en el capítulo 29, fuera del ciclo de petición.

## 31.3 Validación externa y comparación estadística

La validación externa y la comparación estadística se implementan en las funciones `run_external_validation` y `run_statistical_comparison`, que ejecutan los scripts correspondientes del pipeline. La validación externa evalúa los modelos de la sesión sobre el dataset independiente y aplica el test de DeLong; la comparación estadística regenera el ranking y la matriz de Wilcoxon, gestionando el marcador de estado del recálculo. El fragmento siguiente muestra la implementación de la validación externa.

```python
def run_external_validation(session_id, dataset_path):
    base_path = os.getcwd()
    env_vars = os.environ.copy()
    env_vars["TFG_SESSION_ID"] = session_id
    env_vars["TFG_EXTERNAL_DATASET_DIR"] = dataset_path
    script_val = os.path.join(base_path, "pneumoniacnn-main", "code", "4_external_validation.py")
    script_delong = os.path.join(base_path, "pneumoniacnn-main", "code", "5_evaluate_delong.py")
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        subprocess.Popen(["python", script_val], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
        subprocess.Popen(["python", script_delong], stdout=log, stderr=subprocess.STDOUT, env=env_vars, text=True, encoding="utf-8", errors="replace").wait()
```

*Código 31.2 - Validación externa (`services/mlops_engine.py`)*

La implementación de la validación externa refleja la separación entre la validación y la configuración original del experimento: la función recibe la sesión y la ruta del dataset externo, transmite la ruta mediante la variable de entorno `TFG_EXTERNAL_DATASET_DIR` y ejecuta los scripts de validación y del test estadístico de DeLong, que escriben las métricas, la curva ROC y la matriz de DeLong en el subdirectorio `external_validation` de la sesión. La comparación estadística, por su parte, ejecuta el script 3 con el identificador de la sesión, limpia el marcador de estado del recálculo antes de ejecutarlo y lo recrea al finalizar, de modo que la interfaz puede consultar si el recálculo está en curso o completado.

## 31.4 Gestión de las sesiones de experimentación

La gestión de las sesiones se implementa en el motor MLOps, que organiza el directorio de cada sesión en `training_results` y resuelve las operaciones de creación, consulta, renombrado y eliminación. La creación de una sesión materializa el identificador, la configuración y el propietario; la consulta enumera las sesiones del usuario con sus modelos; el renombrado y la eliminación operan sobre el directorio con las comprobaciones de validez y de propiedad. El fragmento siguiente muestra la implementación de la creación de la sesión.

```python
def create_training_session(model_names, dataset_path, epochs, batch_size, learning_rate, user_id=None):
    session_id = f"RUN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_dir = f"training_results/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    with open(os.path.join(session_dir, "dataset_path.txt"), "w", encoding="utf-8") as f:
        f.write(dataset_path)
    config = {"dataset_path": dataset_path, "epochs": epochs, "batch_size": batch_size,
              "learning_rate": learning_rate, "models": [m.strip() for m in model_names.split(",")]}
    if user_id is not None:
        config["user_id"] = user_id
    with open(os.path.join(session_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f)
    return session_id
```

*Código 31.3 - Creación de la sesión de entrenamiento (`services/mlops_engine.py`)*

La implementación de la creación de la sesión refleja la persistencia híbrida del laboratorio: la sesión se materializa en un directorio de `training_results` con su configuración en `config.json` y la ruta del dataset en `dataset_path.txt`. El identificador se genera a partir de la fecha y la hora, y la configuración incorpora los modelos, los hiperparámetros y el identificador del usuario propietario, que la comprobación de propiedad de las sesiones utiliza para aislar los datos entre usuarios. Las operaciones de renombrado y de eliminación operan sobre el directorio mediante el sistema de ficheros, con la sanitización del nuevo nombre y las comprobaciones de existencia y de propiedad descritas en el diseño.

## 31.5 Lectura de los resultados

La lectura de los resultados se implementa en las funciones de consulta del motor, que transforman los artefactos persistidos en el sistema de ficheros en estructuras para la interfaz. La consulta de los resultados de un modelo lee las métricas de validación cruzada, la calibración, las métricas XAI y las rutas de los artefactos visuales; la consulta del ranking lee el ranking por AUC y el heatmap de Wilcoxon; y la consulta de la validación externa lee las métricas, la curva ROC y la matriz de DeLong. El fragmento siguiente muestra la implementación de la lectura del ranking.

```python
def get_session_ranking_data(session_id):
    session_dir = f"training_results/{session_id}"
    csv_path = f"{session_dir}/session_ranking.csv"
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data.append(row)
    heatmap = f"/training_results/{session_id}/wilcoxon_heatmap.png"
    return {"ranking": data, "heatmap": heatmap, "config": read_config(session_dir)}
```

*Código 31.4 - Lectura del ranking de la sesión (`services/mlops_engine.py`)*

La implementación de la lectura de los resultados refleja la decisión de no ejecutar el modelo en las consultas: las funciones transforman los ficheros de resultados persistidos por el pipeline, como los CSV de métricas y los artefactos visuales, en las estructuras que la interfaz presenta, devolviendo `None` cuando los resultados no existen para que el router informe con el código correspondiente. Esta decisión reduce el coste de acceso a los resultados y conserva la separación entre el cálculo y la visualización, en coherencia con el diseño del laboratorio.

## 31.6 Generación del informe de la sesión

La generación del informe de la sesión se implementa en el servicio `pdf_generator_mlops.py`, que compone el documento consolidado mediante la clase `MedicalReport`, especialización de la librería FPDF2 (FPDF2, 2024). El informe recoge la configuración del experimento, el ranking con el heatmap de Wilcoxon, los resultados de la validación externa con la curva ROC y la matriz de DeLong, y el detalle técnico de cada modelo con sus métricas XAI y sus mapas de calor. El fragmento siguiente muestra el inicio de la implementación del generador.

```python
async def generate_pdf_report(session_id):
    session_dir = f"training_results/{session_id}"
    if not os.path.exists(session_dir):
        return JSONResponse(status_code=404, content={"message": "Sesión no encontrada"})

    pdf = MedicalReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.section_title("1. CONFIGURACIÓN DEL SISTEMA Y PARÁMETROS")

    config_path = os.path.join(session_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            cfg = json.load(f)
        # ... secciones de configuración, ranking, Wilcoxon, validación externa y detalle por modelo ...

    pdf_output_path = os.path.join(session_dir, f"Informe_Completo_{session_id}.pdf")
    pdf.output(pdf_output_path)
    return FileResponse(pdf_output_path, filename=f"Reporte_MLOps_{session_id}.pdf")
```

*Código 31.5 - Generación del informe de la sesión (`services/pdf_generator_mlops.py`)*

La implementación del informe refleja la decisión de separar el conocimiento del formato del router: el generador recibe la sesión, lee los artefactos persistidos en el sistema de ficheros, como la configuración, el ranking, los heatmaps, las métricas de la validación externa y las métricas XAI de cada modelo, y compone el documento con la clase `MedicalReport`, que redefine la cabecera corporativa, el pie de página y los títulos de sección. El informe se guarda en el directorio de la sesión y se devuelve como documento descargable; si la sesión no existe, el generador responde HTTP 404.

El laboratorio MLOps de vitalXAI queda codificado en sus funciones principales: el motor orquesta el pipeline de entrenamiento y de validación externa mediante los scripts del proyecto, gestiona las sesiones en el sistema de ficheros, lee los resultados persistidos para la interfaz y genera el informe consolidado de cada sesión. La ejecución experimental documentada sigue siendo parcial, por lo que esta implementación no equivale a un benchmark completo de todas las arquitecturas previstas. La codificación del frontend, que presenta estas capacidades al usuario, se describe en el capítulo siguiente.

---

## Referencias del capítulo

DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: A nonparametric approach. *Biometrics*, 44(3), 837-845.

Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters*, 27(8), 861-874.

He, H., & Garcia, E. A. (2009). Learning from imbalanced data. *IEEE Transactions on Knowledge and Data Engineering*, 21(9), 1263-1284. https://doi.org/10.1109/TKDE.2008.239

Nadeau, C., & Bengio, Y. (2003). Inference for the generalization error. *Machine Learning*, 52, 239-281. https://doi.org/10.1023/A:1024068626366

Varma, S., & Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. *BMC Bioinformatics*, 7, 91. https://doi.org/10.1186/1471-2105-7-91

Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin*, 1(6), 80-83.

Yosinski, J., & al., e. (2014). How transferable are features in deep neural networks? *Advances in Neural Information Processing Systems*, 27, 3320-3328.

Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine learning operations (MLOps): Overview, definition, and architecture. *IEEE Access*, 11, 31866-31879. https://doi.org/10.1109/ACCESS.2023.3262138

Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularization. *International Conference on Learning Representations (ICLR)*. Obtenido de https://arxiv.org/abs/1711.05101

Deng, J., & al., e. (2009). ImageNet: A large-scale hierarchical image database. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 248-255.

Linardatos, P., Papastefanopoulos, V., & Kotsiantis, S. (2021). Explainable AI: A review of machine learning interpretability methods. *Entropy*, 23(1), 18.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the 34th International Conference on Machine Learning*, 1321-1330.

FPDF2. (2024). *FPDF2 Documentation*. Obtenido de https://py-pdf.github.io/fpdf2/
