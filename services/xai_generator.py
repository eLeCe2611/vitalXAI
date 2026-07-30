import matplotlib
import numpy as np
import tensorflow as tf

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from services.lang import get_text
from services.ml_engine import get_model

MODELS_TRANSFORMERS = ["deit", "swin_base", "vit_384"]

def get_img_size(model_name):
    """Devuelve el tamaño de la imagen según la arquitectura."""
    if model_name in ["InceptionV3", "Xception"]:
        return (299, 299)
    elif model_name == "vit_384":
        return (384, 384)
    else:
        return (224, 224)

def load_img_tf(path, img_size):
    """Carga y preprocesa la imagen usando TensorFlow."""
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, img_size)
    return (img / 255.0).numpy()

def get_score(model, img_tf, is_transformer):
    if is_transformer:
        return model(pixel_values=img_tf).logits[0][0]
    else:
        pred = model(img_tf)
        # Bucle de seguridad por si TF devuelve una lista
        if isinstance(pred, list): pred = pred[0]
        return pred[0][0]

def saliency(model, img, is_transformer):
    img_tf = tf.convert_to_tensor(img[None])
    with tf.GradientTape() as tape:
        tape.watch(img_tf)
        score = get_score(model, img_tf, is_transformer)
    grads = tape.gradient(score, img_tf)[0]
    sal = tf.reduce_max(tf.abs(grads), axis=-1)
    return sal.numpy()

def smoothgrad(model, img, is_transformer, n_samples=30, noise=0.1):
    H, W, C = img.shape
    acc = np.zeros((H, W))
    for _ in range(n_samples):
        noisy = img + np.random.normal(0, noise, img.shape)
        noisy = np.clip(noisy, 0, 1)
        acc += saliency(model, noisy, is_transformer)
    sm = acc / n_samples
    sm = (sm - sm.min()) / (sm.max() - sm.min() + 1e-9)
    return sm

def get_cam_or_attention(model, img, is_transformer, img_size):
    """Bifurcación de XAI dependiendo de la arquitectura."""
    if not is_transformer:
        target = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                target = layer.name
                break
        if target is None:
            return np.zeros((img_size[0], img_size[1]))

        grad_model = tf.keras.Model(model.inputs, [model.get_layer(target).output, model.output])
        with tf.GradientTape() as tape:
            img_tensor = tf.convert_to_tensor(img[None])
            conv, pred = grad_model(img_tensor)

            # --- FIX DEL BUG ---
            # Si TF envuelve los resultados en listas, los extraemos
            if isinstance(conv, list): conv = conv[0]
            if isinstance(pred, list): pred = pred[0]
            # -------------------

            loss = pred[:, 0]
        grads = tape.gradient(loss, conv)[0]
        weights = tf.reduce_mean(grads, axis=(0,1))
        cam = tf.reduce_sum(weights * conv[0], axis=-1)
        cam = np.maximum(cam, 0)
        cam = cam / (cam.max() + 1e-9)
        return tf.image.resize(cam[..., None], img_size).numpy().squeeze()

    else:
        img_tf = tf.convert_to_tensor(img[None])
        try:
            outputs = model(pixel_values=img_tf, output_attentions=True)
            attn_layer = outputs.attentions[-1]
            attn_heads = tf.reduce_mean(attn_layer, axis=1)[0]
            cls_attn = attn_heads[0, 1:]
            grid_size = int(np.sqrt(cls_attn.shape[0]))
            attn_grid = tf.reshape(cls_attn, (grid_size, grid_size))
            attn_map = tf.image.resize(attn_grid[..., None], img_size).numpy().squeeze()
            return (attn_map - attn_map.min()) / (attn_map.max() - attn_map.min() + 1e-9)
        except Exception:
            with tf.GradientTape() as tape:
                tape.watch(img_tf)
                score = model(pixel_values=img_tf).logits[0][0]
            grads = tape.gradient(score, img_tf)[0]
            gxi = tf.reduce_max(tf.abs(grads * img_tf[0]), axis=-1).numpy()
            return (gxi - gxi.min()) / (gxi.max() - gxi.min() + 1e-9)

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

    plt.subplot(1, 4, 2)
    plt.imshow(sal, cmap="inferno")
    plt.title(get_text("xai_saliency", lang), fontsize=12)
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.imshow(sm, cmap="inferno")
    plt.title(get_text("xai_smoothgrad", lang), fontsize=12)
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.imshow(img, alpha=0.5)
    plt.imshow(cam, cmap="jet", alpha=0.5)
    plt.title(get_text("xai_overlay", lang).format(method=xai_method_name), fontsize=12)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(xai_save_path, bbox_inches='tight', dpi=150)
    plt.close()

    return xai_save_path
