import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USE_TF"] = "1"

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
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
# CARGA DEL MODELO
# ==========================================
if IS_TRANSFORMER:
    model = TFAutoModelForImageClassification.from_pretrained(TRANSFORMERS[MODEL_NAME], num_labels=1, ignore_mismatched_sizes=True)
    model.load_weights(f"{OUTPUT_DIR}/best_fold1.weights.h5")
else:
    model = tf.keras.models.load_model(f"{OUTPUT_DIR}/best_fold1.keras", compile=False)

# ==========================================
# ALGORITMOS XAI
# ==========================================
def get_saliency_map(img_tensor):
    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        preds = model(**{"pixel_values": img_tensor}).logits if IS_TRANSFORMER else model(img_tensor)
        loss = preds[:, 0]

    grads = tape.gradient(loss, img_tensor)
    grads = tf.reduce_max(tf.abs(grads), axis=1) if IS_TRANSFORMER else tf.reduce_max(tf.abs(grads), axis=-1)

    saliency = grads[0].numpy()
    return (saliency - np.min(saliency)) / (np.max(saliency) + 1e-10)

def get_gradcam(img_tensor):
    # Encontrar la última capa convolucional de la CNN
    last_conv_layer = None
    for layer in reversed(model.layers):
        if len(layer.output_shape) == 4: # Normalmente las Conv2D tienen shape (None, H, W, C)
            last_conv_layer = layer.name
            break

    if not last_conv_layer:
        return np.zeros((IMG_SIZE[0], IMG_SIZE[1]))

    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor)
        loss = predictions[:, 0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap).numpy()
    heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-10)

    return heatmap

def load_and_prep_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img, IMG_SIZE) / 255.0

    if IS_TRANSFORMER:
        img_input = np.transpose(img_resized, (2, 0, 1))
        img_input = np.expand_dims(img_input, axis=0)
    else:
        img_input = np.expand_dims(img_resized, axis=0)

    return img, tf.convert_to_tensor(img_input, dtype=tf.float32)

# ==========================================
# GENERACIÓN VISUAL
# ==========================================
def main():
    pneu_dir = os.path.join(DATASET_DIR, "PNEUMONIA")
    sample_images = [os.path.join(pneu_dir, f) for f in os.listdir(pneu_dir)[:8]]

    for i, path in enumerate(sample_images):
        orig_img, input_img = load_and_prep_image(path)
        saliency = get_saliency_map(input_img)

        plt.figure(figsize=(20, 5))

        if IS_TRANSFORMER:
            # Los Transformers solo muestran Original y Saliency
            saliency_resized = cv2.resize(saliency, (orig_img.shape[1], orig_img.shape[0]))

            plt.subplot(1, 4, 1)
            plt.imshow(orig_img)
            plt.title("Original")
            plt.axis("off")

            plt.subplot(1, 4, 2)
            plt.imshow(saliency, cmap='magma')
            plt.title("Saliency (Atención Transformer)")
            plt.axis("off")

            plt.subplot(1, 4, 3)
            plt.imshow(orig_img)
            plt.imshow(saliency_resized, cmap='jet', alpha=0.5)
            plt.title("Saliency Superpuesta")
            plt.axis("off")

            plt.subplot(1, 4, 4)
            plt.axis("off")

        else:
            # Las CNNs vuelven a su formato original de 4 paneles con Grad-CAM
            heatmap = get_gradcam(input_img)
            heatmap_resized = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
            heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
            heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

            # --- CORRECCIÓN CLAVE AQUÍ: Se eliminó el / 255.0 ---
            superimposed = cv2.addWeighted(orig_img, 0.6, heatmap_color, 0.4, 0)

            plt.subplot(1, 4, 1)
            plt.imshow(orig_img)
            plt.title("Original")
            plt.axis("off")

            plt.subplot(1, 4, 2)
            plt.imshow(saliency, cmap='magma')
            plt.title("Saliency Map")
            plt.axis("off")

            plt.subplot(1, 4, 3)
            plt.imshow(heatmap_resized, cmap='inferno')
            plt.title("Grad-CAM")
            plt.axis("off")

            plt.subplot(1, 4, 4)
            plt.imshow(superimposed)
            plt.title("Superposición Grad-CAM")
            plt.axis("off")

        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/xai_example_{i+1}.png", bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    main()
