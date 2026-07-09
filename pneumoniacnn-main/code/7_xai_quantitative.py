import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USE_TF"] = "1"

import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import cv2
from sklearn.metrics import auc, brier_score_loss
from transformers import TFAutoModelForImageClassification

SESSION_ID = os.getenv("TFG_SESSION_ID")
MODEL_NAME = os.getenv("TFG_MODEL_NAME")
DATASET_DIR = os.getenv("TFG_DATASET_DIR")
OUTPUT_DIR = f"training_results/{SESSION_ID}/{MODEL_NAME}"

TRANSFORMERS = {
    "deit": "facebook/deit-base-distilled-patch16-224",
    "swin_base": "microsoft/swin-base-patch4-window7-224",
    "vit_384": "google/vit-base-patch16-384"
}
IS_TRANSFORMER = MODEL_NAME in TRANSFORMERS
IMG_SIZE = (384, 384) if MODEL_NAME == "vit_384" else (224, 224)

# ==========================================
# 1. CARGAR MODELO
# ==========================================
if IS_TRANSFORMER:
    model = TFAutoModelForImageClassification.from_pretrained(TRANSFORMERS[MODEL_NAME], num_labels=1, ignore_mismatched_sizes=True)
    model.load_weights(f"{OUTPUT_DIR}/best_fold1.weights.h5")
else:
    model = tf.keras.models.load_model(f"{OUTPUT_DIR}/best_fold1.keras", compile=False)

# ==========================================
# 2. FUNCIONES MATEMÁTICAS XAI
# ==========================================
def predict_prob(img_tensor):
    if IS_TRANSFORMER:
        logits = model(**{"pixel_values": img_tensor}).logits
        return tf.nn.sigmoid(logits[:, 0]).numpy()[0]
    else:
        return model.predict(img_tensor, verbose=0)[0][0]

def get_xai_map(img_tensor):
    if IS_TRANSFORMER:
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            preds = model(**{"pixel_values": img_tensor}).logits
            loss = preds[:, 0]
        grads = tape.gradient(loss, img_tensor)
        saliency = tf.reduce_max(tf.abs(grads), axis=1)[0].numpy()
        return (saliency - np.min(saliency)) / (np.max(saliency) + 1e-10)
    else:
        last_conv_layer = None
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:
                last_conv_layer = layer.name
                break
        if not last_conv_layer: return np.zeros((IMG_SIZE[0], IMG_SIZE[1]))

        grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(last_conv_layer).output, model.output])
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_tensor)
            loss = predictions[:, 0]
        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = conv_outputs[0] @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap).numpy()
        heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-10)
        return cv2.resize(heatmap, IMG_SIZE)

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE) / 255.0
    if IS_TRANSFORMER:
        return np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)
    return np.expand_dims(img, axis=0)

def calculate_insertion_deletion(img_input, xai_map, steps=10):
    original_prob = predict_prob(tf.convert_to_tensor(img_input, dtype=tf.float32))
    flat_map = xai_map.flatten()
    sorted_indices = np.argsort(flat_map)[::-1]
    n_pixels = len(sorted_indices)
    step_size = n_pixels // steps
    
    deletion_probs, insertion_probs = [original_prob], [0.0]
    
    if IS_TRANSFORMER:
        del_img, img_flat = img_input.copy().reshape(3, -1), img_input.copy().reshape(3, -1)
    else:
        del_img, img_flat = img_input.copy().reshape(-1, 3), img_input.copy().reshape(-1, 3)
    
    ins_img = np.zeros_like(del_img)

    for i in range(1, steps + 1):
        idx_to_modify = sorted_indices[:i * step_size]
        
        del_temp = del_img.copy()
        ins_temp = ins_img.copy()
        
        if IS_TRANSFORMER:
            del_temp[:, idx_to_modify] = 0
            ins_temp[:, idx_to_modify] = img_flat[:, idx_to_modify]
            del_tensor = tf.convert_to_tensor(del_temp.reshape(1, 3, IMG_SIZE[0], IMG_SIZE[1]), dtype=tf.float32)
            ins_tensor = tf.convert_to_tensor(ins_temp.reshape(1, 3, IMG_SIZE[0], IMG_SIZE[1]), dtype=tf.float32)
        else:
            del_temp[idx_to_modify, :] = 0
            ins_temp[idx_to_modify, :] = img_flat[idx_to_modify, :]
            del_tensor = tf.convert_to_tensor(del_temp.reshape(1, IMG_SIZE[0], IMG_SIZE[1], 3), dtype=tf.float32)
            ins_tensor = tf.convert_to_tensor(ins_temp.reshape(1, IMG_SIZE[0], IMG_SIZE[1], 3), dtype=tf.float32)
            
        deletion_probs.append(predict_prob(del_tensor))
        insertion_probs.append(predict_prob(ins_tensor))

    x_axis = np.linspace(0, 1, steps + 1)
    return auc(x_axis, deletion_probs), auc(x_axis, insertion_probs), (np.cumsum(flat_map[sorted_indices]) / np.sum(flat_map) < 0.9).mean()

def calculate_entropy(xai_map):
    """Calcula la Entropía de Shannon del mapa de calor."""
    p = xai_map.flatten()
    p = p / (np.sum(p) + 1e-10)
    p = p[p > 0] # Eliminar ceros para no romper el logaritmo
    return -np.sum(p * np.log2(p))

def calculate_stability(img_input, original_map):
    """Calcula la estabilidad inyectando ruido gaussiano en la imagen original."""
    img_tensor = tf.convert_to_tensor(img_input, dtype=tf.float32)
    noise = tf.random.normal(shape=tf.shape(img_tensor), mean=0.0, stddev=0.05) # 5% de ruido
    noisy_img_tensor = tf.clip_by_value(img_tensor + noise, 0.0, 1.0)
    
    noisy_map = get_xai_map(noisy_img_tensor)
    
    # Error Cuadrático Medio entre el mapa original y el mapa de la imagen con ruido
    mse = np.mean((original_map - noisy_map) ** 2)
    # Lo invertimos para que mayor = mejor (de 0 a 1)
    return 1.0 / (1.0 + (mse * 10))

def calculate_ece(y_true, y_prob, n_bins=10):
    """Calcula el Expected Calibration Error (ECE)"""
    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        in_bin = np.where((y_prob >= bin_edges[i]) & (y_prob <= bin_edges[i+1]))[0]
        if len(in_bin) > 0:
            acc = np.mean(y_true[in_bin] == (y_prob[in_bin] >= 0.5))
            conf = np.mean(y_prob[in_bin])
            ece += (len(in_bin) / len(y_prob)) * np.abs(acc - conf)
    return ece

# ==========================================
# 3. EJECUCIÓN
# ==========================================
def main():
    print(f"[XAI AUTO] Calculando métricas cuantitativas REALES para {MODEL_NAME}...")
    
    # 1. EVALUACIÓN DE CALIBRACIÓN (10 imágenes: 5 Normales, 5 Neumonías)
    norm_dir = os.path.join(DATASET_DIR, "NORMAL")
    pneu_dir = os.path.join(DATASET_DIR, "PNEUMONIA")
    
    calib_images = [os.path.join(norm_dir, f) for f in os.listdir(norm_dir)[:5]] + \
                   [os.path.join(pneu_dir, f) for f in os.listdir(pneu_dir)[:5]]
    y_true_calib = np.array([0]*5 + [1]*5)
    y_prob_calib = []
    
    for path in calib_images:
        img_input = preprocess_image(path)
        img_tensor = tf.convert_to_tensor(img_input, dtype=tf.float32)
        y_prob_calib.append(predict_prob(img_tensor))
        
    y_prob_calib = np.array(y_prob_calib)
    
    brier = brier_score_loss(y_true_calib, y_prob_calib)
    ece = calculate_ece(y_true_calib, y_prob_calib)
    
    with open(f"{OUTPUT_DIR}/calibration_metrics.txt", "w") as f:
        f.write(f"Brier Score: {brier:.4f}\nECE Score: {ece:.4f}\n")

    # 2. EVALUACIÓN DE EXPLICABILIDAD (5 imágenes Neumonía)
    xai_images = [os.path.join(pneu_dir, f) for f in os.listdir(pneu_dir)[:5]]
    
    d_aucs, i_aucs, sparsities, entropies, stabilities = [], [], [], [], []
    
    for path in xai_images:
        img_input = preprocess_image(path)
        img_tensor = tf.convert_to_tensor(img_input, dtype=tf.float32)
        xai_map = get_xai_map(img_tensor)
        
        d_auc, i_auc, spars = calculate_insertion_deletion(img_input, xai_map, steps=10)
        entr = calculate_entropy(xai_map)
        stab = calculate_stability(img_input, xai_map)
        
        d_aucs.append(d_auc)
        i_aucs.append(i_auc)
        sparsities.append(spars)
        entropies.append(entr)
        stabilities.append(stab)
        
    method_name = "Saliency Map" if IS_TRANSFORMER else "Grad-CAM"
    
    metrics_data = [{
        "Method": method_name,
        "deletion_auc": f"{np.mean(d_aucs):.4f} ± {np.std(d_aucs):.4f}",
        "insertion_auc": f"{np.mean(i_aucs):.4f} ± {np.std(i_aucs):.4f}",
        "sparsity": f"{np.mean(sparsities):.4f} ± {np.std(sparsities):.4f}",
        "entropy": f"{np.mean(entropies):.4f} ± {np.std(entropies):.4f}",
        "stability": f"{np.mean(stabilities):.4f} ± {np.std(stabilities):.4f}"
    }]
    
    df = pd.DataFrame(metrics_data)
    df.to_csv(f"{OUTPUT_DIR}/xai_metrics_comparison.csv", index=False)
    print("[XAI AUTO] Métricas cuantitativas completadas.")

if __name__ == "__main__":
    main()