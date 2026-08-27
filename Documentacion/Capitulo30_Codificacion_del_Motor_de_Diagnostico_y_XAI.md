# Capítulo 30: Codificación del motor de diagnóstico y XAI

El motor de diagnóstico y de explicabilidad constituye el núcleo clínico de vitalXAI: recibe una radiografía de tórax, produce la predicción de neumonía con su nivel de confianza y genera los mapas de calor que explican la decisión del modelo, además del informe PDF de la consulta. Este capítulo describe la codificación de este motor, que se materializa en tres servicios: `ml_engine.py`, que carga los modelos y ejecuta la predicción; `xai_generator.py`, que genera los mapas de explicabilidad; y `pdf_generator.py`, que construye el informe del diagnóstico. La implementación se organiza en cuatro apartados: la carga y la caché de los modelos, el preprocesado y la predicción, la generación de los mapas de explicabilidad y la generación del informe PDF.

El motor se apoya en las librerías de aprendizaje profundo y de visión por computador descritas en el entorno de construcción del capítulo 23: TensorFlow y la librería Transformers de Hugging Face para la carga de las arquitecturas, OpenCV para el preprocesado de las imágenes y FPDF para la generación del informe (TensorFlow, 2024; Hugging Face, 2024). La implementación distingue dos familias de arquitecturas —las convolucionales (CNN) y las Transformer—, cuyas decisiones de carga, preprocesado e inferencia se bifurcan en cada servicio, en coherencia con el diseño del subsistema SD-002 descrito en el capítulo 17.

## 30.1 Carga y caché de los modelos

La carga de los modelos se implementa en el servicio `ml_engine.py`, que diferencia el procedimiento según la familia de la arquitectura. Los modelos convolucionales se cargan desde sus pesos entrenados en formato Keras; los modelos Transformer se cargan desde su arquitectura preentrenada de Hugging Face y, a continuación, se aplican los pesos entrenados del proyecto. En ambos casos, el modelo se conserva en un diccionario global de caché, de modo que la primera consulta con cada arquitectura paga la carga de los pesos y las posteriores reutilizan el modelo en memoria. El fragmento siguiente muestra la implementación de la carga.

```python
loaded_models = {}
MODELS_TRANSFORMERS = ["deit", "swin_base", "vit_384"]
HF_MODEL_IDS = {
    "deit": "facebook/deit-base-distilled-patch16-224",
    "swin_base": "microsoft/swin-base-patch4-window7-224",
    "vit_384": "google/vit-base-patch16-384",
}

def get_model(model_name: str):
    if model_name not in loaded_models:
        is_transformer = model_name in MODELS_TRANSFORMERS

        if is_transformer:
            from transformers import TFAutoModelForImageClassification
            model_path = os.path.join("pneumoniacnn-main", "results", model_name, "best_fold1.h5")
            if not os.path.exists(model_path):
                model_path = os.path.join("pneumoniacnn-main", "results", model_name, "best_fold1.weights.h5")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Pesos de Transformer no encontrados en: {model_path}")

            model = TFAutoModelForImageClassification.from_pretrained(
                HF_MODEL_IDS[model_name], num_labels=1, ignore_mismatched_sizes=True, output_attentions=True
            )
            model.load_weights(model_path)
            loaded_models[model_name] = model
        else:
            model_path = os.path.join("pneumoniacnn-main", "results", model_name, "best_fold1.keras")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelo CNN no encontrado en: {model_path}")
            loaded_models[model_name] = load_model(model_path)

    return loaded_models[model_name]
```

*Código 30.1 - Carga y caché de los modelos (`services/ml_engine.py`)*

La implementación de la carga refleja las decisiones del diseño del motor. La diferenciación por familia permite cargar cada arquitectura con el procedimiento adecuado: las CNN se cargan directamente con el cargador de modelos de Keras, y los Transformer se construyen sobre la arquitectura de Hugging Face, con la salida de atención habilitada para la generación de los mapas de explicabilidad, y reciben los pesos entrenados del proyecto. La caché en memoria implementa el requisito de tiempo de respuesta de la inferencia (RNF-019): la primera consulta con cada arquitectura asume el coste de la carga, mientras que las posteriores reutilizan el modelo. La ausencia de los pesos se resuelve con un error explícito, de modo que un modelo no disponible falla antes de producir un resultado ambiguo, tal y como se declaró en el diseño.

## 30.2 Preprocesado y predicción

La predicción se implementa en la función `process_and_predict`, que prepara la imagen según la arquitectura y ejecuta la inferencia. El preprocesado ajusta la resolución de entrada a la arquitectura seleccionada —299×299 para InceptionV3 y Xception, 384×384 para ViT-384 y 224×224 para el resto—, convierte la imagen al espacio RGB y la normaliza. La inferencia se bifurca por familia: los Transformer procesan la imagen con los `pixel_values` y aplican una sigmoide sobre el logit, mientras que las CNN utilizan la predicción directa del modelo. El fragmento siguiente muestra la implementación del preprocesado y de la inferencia.

```python
def process_and_predict(model_name: str, image_path: str, lang: str = "es"):
    model = get_model(model_name)
    is_transformer = model_name in MODELS_TRANSFORMERS

    if model_name in ["InceptionV3", "Xception"]:
        img_size = (299, 299)
    elif model_name == "vit_384":
        img_size = (384, 384)
    else:
        img_size = (224, 224)

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, img_size)
    img_array = img_resized / 255.0
    img_tensor = np.expand_dims(img_array, axis=0)

    if is_transformer:
        img_tensor_tf = tf.convert_to_tensor(img_tensor, dtype=tf.float32)
        logits = model(pixel_values=img_tensor_tf).logits
        prediction = float(tf.nn.sigmoid(logits)[0][0])
    else:
        prediction = float(model.predict(img_tensor, verbose=0)[0][0])

    is_pneumonia = prediction > 0.5
    label = get_text("label_pneumonia", lang) if is_pneumonia else get_text("label_normal", lang)
    confidence = prediction if is_pneumonia else (1 - prediction)
    confidence_percent = round(confidence * 100, 2)

    return label, confidence_percent
```

*Código 30.2 - Preprocesado y predicción (`services/ml_engine.py`)*

La implementación de la predicción refleja las decisiones del diseño clínico. La normalización divide los píxeles entre 255 para escalarlos al intervalo de entrada de los modelos; la inferencia devuelve la probabilidad de la clase neumonía, y el umbral de 0.5 decide la etiqueta de la predicción. La confianza se expresa en el intervalo 0-100: para la clase neumonía coincide con la probabilidad, y para la clase normal se calcula como su complementaria, de modo que la confianza siempre refleja la seguridad de la predicción emitida. Las etiquetas se localizan mediante el servicio de idioma, en coherencia con la internacionalización de la plataforma.

## 30.3 Generación de los mapas de explicabilidad

La generación de los mapas de explicabilidad se implementa en el servicio `xai_generator.py`, que calcula los tres mapas de la explicación visual y compone la figura con la radiografía original. Para las arquitecturas convolucionales se aplican los métodos basados en gradientes —Saliency, SmoothGrad y Grad-CAM—, mientras que para las Transformer se utiliza el mapa de atención de la última capa, con un respaldo basado en gradientes ante un fallo del cálculo de la atención. El fragmento siguiente muestra la implementación de la generación del mapa de explicabilidad.

```python
def generate_xai_heatmap(model_name: str, original_image_path: str, xai_save_path: str, lang: str = "es"):
    model = get_model(model_name)
    is_transformer = model_name in MODELS_TRANSFORMERS
    img_size = get_img_size(model_name)
    xai_method_name = "Attention Map" if is_transformer else "Grad-CAM"

    img = load_img_tf(original_image_path, img_size)
    sal = saliency(model, img, is_transformer)
    sm = smoothgrad(model, img, is_transformer)
    cam = get_cam_or_attention(model, img, is_transformer, img_size)

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 4, 1)
    plt.imshow(img)
    plt.title(get_text("xai_original", lang), fontsize=12)
    plt.axis("off")
    # ... subplots de Saliency, SmoothGrad y la superposición del Grad-CAM o la atención ...
    plt.tight_layout()
    plt.savefig(xai_save_path, bbox_inches="tight", dpi=150)
    plt.close()
    return xai_save_path
```

*Código 30.3 - Generación del mapa de explicabilidad (`services/xai_generator.py`)*

La implementación de la explicabilidad refleja las decisiones del diseño del subsistema de diagnóstico. El mapa de Saliency se calcula mediante los gradientes de la puntuación de la clase respecto a la imagen, aplicados con una cinta de gradientes de TensorFlow; el mapa de SmoothGrad promedia treinta mapas de Saliency con ruido gaussiano y normaliza el resultado; y el mapa de Grad-CAM pondera las activaciones de la última capa convolucional por los gradientes, mientras que las Transformer producen un mapa de atención a partir de la última capa de atención. La figura resultante combina la radiografía original, el Saliency, el SmoothGrad y la superposición del mapa principal, se guarda con el backend no interactivo de matplotlib y se persiste su ruta en la consulta, de modo que las visualizaciones posteriores no repiten el cálculo.

## 30.4 Generación del informe PDF

La generación del informe PDF se implementa en el servicio `pdf_generator.py`, que compone el documento de la consulta mediante la clase `PDFReport`, especialización de la librería FPDF. El informe incluye la fecha, el modelo utilizado, el diagnóstico con su color según el resultado, el nivel de confianza y las dos imágenes —la radiografía original y el mapa de explicabilidad—. El fragmento siguiente muestra la implementación de la generación del informe.

```python
def generate_medical_report(image_path, xai_path, label, confidence, model_name, lang="es"):
    pdf = PDFReport(lang=lang)
    pdf.add_page()
    pdf.set_font("helvetica", "", 12)

    pdf.cell(0, 10, f" {get_text('pdf_date', lang)} {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    pdf.cell(0, 10, f" {get_text('pdf_model', lang)} {model_name}")
    pdf.ln(10)

    pdf.set_font("helvetica", "B", 14)
    if "neumonía" in label.lower() or "pneumonia" in label.lower() or "肺炎" in label or "न्यूमोनिया" in label:
        pdf.set_text_color(192, 57, 43)
    else:
        pdf.set_text_color(39, 174, 96)

    pdf.cell(0, 10, get_text("pdf_diagnosis", lang).format(label=label.upper()))
    pdf.set_text_color(0)
    pdf.cell(0, 10, get_text("pdf_confidence", lang).format(confidence=confidence))
    pdf.ln(10)

    try:
        pdf.image(image_path, 20, 100, 70)
        pdf.image(xai_path, 110, 100, 70)
    except Exception:
        pdf.cell(0, 10, get_text("pdf_error_images", lang))

    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("static", "reports", filename)
    pdf.output(filepath, "F")
    return filepath
```

*Código 30.4 - Generación del informe PDF (`services/pdf_generator.py`)*

La implementación del informe refleja las decisiones del diseño del CU-037. El documento se compone con la clase `PDFReport`, que hereda de la librería y redefine la cabecera y el pie de página; el color del diagnóstico se determina según el resultado —rojo para la neumonía y verde para el resultado normal—, considerando las etiquetas en los idiomas soportados. Las imágenes se insertan en paralelo y, si la carga de alguna falla, se muestra un texto de error en su lugar, de modo que el documento no queda incompleto. El informe se guarda en el área de informes con un nombre basado en la fecha y se devuelve la ruta, que se persiste en la consulta para su descarga posterior.

El motor de diagnóstico y de explicabilidad de vitalXAI queda así codificado de forma completa: la carga y la caché de los modelos atienden la inferencia con las dos familias de arquitecturas, el preprocesado y la predicción producen la etiqueta y la confianza, la generación de los mapas de explicabilidad proporciona la justificación visual de la decisión y la generación del informe PDF materializa el documento de la consulta. Estos servicios, invocados por el worker de la cola descrito en el capítulo 29, constituyen el núcleo clínico de la plataforma; la codificación del laboratorio de experimentación MLOps se describe en el capítulo siguiente.
