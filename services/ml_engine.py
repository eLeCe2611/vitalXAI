import os

os.environ['USE_TF'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# trainer.py establece TF_USE_LEGACY_KERAS=1 para los scripts de entrenamiento,
# pero los modelos están guardados en formato Keras 3. Lo eliminamos aquí
# para que TF cargue con Keras 3 nativo.
os.environ.pop('TF_USE_LEGACY_KERAS', None)

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Caché de modelos y configuración de Transformers
loaded_models = {}
MODELS_TRANSFORMERS = ["deit", "swin_base", "vit_384"]
HF_MODEL_IDS = {
    "deit": "facebook/deit-base-distilled-patch16-224",
    "swin_base": "microsoft/swin-base-patch4-window7-224",
    "vit_384": "google/vit-base-patch16-384"
}

def get_model(model_name: str):
    """Carga el modelo en memoria diferenciando entre CNN y Transformer."""
    if model_name not in loaded_models:
        is_transformer = model_name in MODELS_TRANSFORMERS

        if is_transformer:
            # BYPASS DE IMPORTACIÓN: Vamos directamente al archivo fuente interno
            try:
                from transformers import TFAutoModelForImageClassification
            except ImportError:
                from transformers.models.auto.modeling_tf_auto import TFAutoModelForImageClassification

            # 1. Carga de Transformer (HuggingFace)
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
            # 2. Carga de CNN clásica (Keras)
            model_path = os.path.join("pneumoniacnn-main", "results", model_name, "best_fold1.keras")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelo CNN no encontrado en: {model_path}")
            loaded_models[model_name] = load_model(model_path)

    return loaded_models[model_name]

def process_and_predict(model_name: str, image_path: str):
    """Preprocesa la imagen y devuelve la predicción según la arquitectura."""
    model = get_model(model_name)
    is_transformer = model_name in MODELS_TRANSFORMERS

    # Ajuste de resolución dinámico
    if model_name in ["InceptionV3", "Xception"]:
        img_size = (299, 299)
    elif model_name == "vit_384":
        img_size = (384, 384)
    else:
        img_size = (224, 224)

    # Preprocesado OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, img_size)
    img_array = img_resized / 255.0
    img_tensor = np.expand_dims(img_array, axis=0)

    # Inferencia bifurcada
    if is_transformer:
        img_tensor_tf = tf.convert_to_tensor(img_tensor, dtype=tf.float32)
        logits = model(pixel_values=img_tensor_tf).logits
        prediction = float(tf.nn.sigmoid(logits)[0][0])
    else:
        prediction = float(model.predict(img_tensor, verbose=0)[0][0])

    # Lógica de confianza
    is_pneumonia = prediction > 0.5
    label = "Neumonía" if is_pneumonia else "Normal"
    confidence = prediction if is_pneumonia else (1 - prediction)
    confidence_percent = round(confidence * 100, 2)

    return label, confidence_percent
