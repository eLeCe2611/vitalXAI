import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USE_TF"] = "1"

import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from transformers import TFAutoModelForImageClassification

SESSION_ID = os.getenv("TFG_SESSION_ID")
EXTERNAL_DATASET_DIR = os.getenv("TFG_EXTERNAL_DATASET_DIR")
SESSION_DIR = f"training_results/{SESSION_ID}"
OUTPUT_DIR = f"{SESSION_DIR}/external_validation"

if not SESSION_ID or not EXTERNAL_DATASET_DIR:
    print("[ERROR] Faltan variables de entorno.")
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

TRANSFORMERS = {
    "deit": "facebook/deit-base-distilled-patch16-224",
    "swin_base": "microsoft/swin-base-patch4-window7-224",
    "vit_384": "google/vit-base-patch16-384"
}

# --- MEJORA: Filtro inteligente de modelos ---
def get_models_in_session():
    valid_models = []
    if os.path.exists(SESSION_DIR):
        for item in os.listdir(SESSION_DIR):
            item_path = os.path.join(SESSION_DIR, item)
            # Solo consideramos que es un modelo si tiene su CSV de resultados K-Fold
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "kfold_results.csv")):
                valid_models.append(item)
    return valid_models

def load_external_data(model_name):
    # Adaptación de tamaño de imagen según la arquitectura
    img_size = (224, 224)
    if model_name == "vit_384": img_size = (384, 384)
    elif model_name == "NASNetLarge": img_size = (331, 331)
    elif model_name in ["InceptionV3", "Xception", "InceptionResNetV2"]: img_size = (299, 299)

    is_transformer = model_name in TRANSFORMERS

    images, labels = [], []
    for cls, label in [("NORMAL", 0), ("PNEUMONIA", 1)]:
        class_dir = os.path.join(EXTERNAL_DATASET_DIR, cls)
        if not os.path.isdir(class_dir): continue
        for f in os.listdir(class_dir):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(class_dir, f)
                img = cv2.imread(path)
                if img is None: continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, img_size) / 255.0

                if is_transformer:
                    # Transformers usan formato Canales-Alto-Ancho (C, H, W)
                    img = np.transpose(img, (2, 0, 1))

                images.append(img)
                labels.append(label)

    return np.array(images, dtype=np.float32), np.array(labels, dtype=np.int32)

def main():
    print(f"\n[VALIDACION EXTERNA] Iniciando evaluacion en dataset: {EXTERNAL_DATASET_DIR}")

    models_to_evaluate = get_models_in_session()
    if not models_to_evaluate:
        print("[ERROR] No se encontraron modelos validos en la sesion.")
        sys.exit(1)

    metrics_list = []
    all_predictions = {}

    plt.figure(figsize=(8, 6))

    for model_name in models_to_evaluate:
        print(f"\n--- Evaluando {model_name} ---")
        model_dir = os.path.join(SESSION_DIR, model_name)

        h5_path = f"{model_dir}/best_fold1.weights.h5"
        keras_path = f"{model_dir}/best_fold1.keras"

        is_transformer = model_name in TRANSFORMERS

        try:
            X_test, y_true = load_external_data(model_name)

            if is_transformer:
                model = TFAutoModelForImageClassification.from_pretrained(TRANSFORMERS[model_name], num_labels=1, ignore_mismatched_sizes=True)
                model.load_weights(h5_path)

                y_prob = []
                batch_size = 16
                for i in range(0, len(X_test), batch_size):
                    batch = X_test[i:i+batch_size]
                    logits = model(**{"pixel_values": tf.constant(batch)}).logits
                    probs = tf.nn.sigmoid(logits).numpy().ravel()
                    y_prob.extend(probs)
                y_prob = np.array(y_prob)

            else:
                model = tf.keras.models.load_model(keras_path, compile=False)
                y_prob = model.predict(X_test, batch_size=32).ravel()

            y_pred = (y_prob >= 0.5).astype(int)

            all_predictions[f"prob_{model_name}"] = y_prob

            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, zero_division=0)
            rec = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            auc = roc_auc_score(y_true, y_prob)

            metrics_list.append({
                "Model": model_name, "Accuracy": acc, "Precision": prec,
                "Recall": rec, "F1-score": f1, "AUC": auc
            })

            fpr, tpr, _ = roc_curve(y_true, y_prob)
            plt.plot(fpr, tpr, label=f"{model_name} (AUC = {auc:.4f})")

            print(f"[OK] {model_name} completado: AUC = {auc:.4f}")

        except Exception as e:
            # Quitamos el emoji para que Windows no crashee
            print(f"[ERROR] Fallo al evaluar {model_name}: {str(e)}")

        finally:
            tf.keras.backend.clear_session()

    if not metrics_list:
        print("[ERROR] Ningun modelo pudo ser evaluado.")
        sys.exit(1)

    # Guardar CSV de métricas
    df_metrics = pd.DataFrame(metrics_list).sort_values(by="AUC", ascending=False)
    df_metrics.to_csv(f"{OUTPUT_DIR}/external_validation_metrics.csv", index=False)

    # Guardar CSV de predicciones (Para DeLong - Script 5)
    if all_predictions:
        all_predictions['y_true'] = y_true
        # Aseguramos que el nombre coincida con lo que espera el Test de DeLong
        pd.DataFrame(all_predictions).to_csv(f"{OUTPUT_DIR}/external_raw_probabilities.csv", index=False)

    # Guardar Gráfico ROC
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Curvas ROC (Dataset Externo)')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/roc_external_validation.png", bbox_inches='tight', dpi=300)
    plt.close()

    print("\n[EXITO] Validacion externa completada y guardada.")

if __name__ == "__main__":
    main()
