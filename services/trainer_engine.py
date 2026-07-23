import json
import os
import traceback
from datetime import datetime

import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.optimizers import Adam

from database import get_db_connection

# ======================================================
# CONFIGURATION
# ======================================================
AUTOTUNE = tf.data.AUTOTUNE

def get_img_size(model_name):
    mn = model_name.lower().replace(" ", "")

    # EfficientNet B0-B7
    if "efficientnetb" in mn:
        if "b1" in mn: return (240, 240)
        if "b2" in mn: return (260, 260)
        if "b3" in mn: return (300, 300)
        if "b4" in mn: return (380, 380)
        if "b5" in mn: return (456, 456)
        if "b6" in mn: return (528, 528)
        if "b7" in mn: return (600, 600)
        return (224, 224) # B0 default

    # EfficientNetV2
    if "efficientnetv2" in mn:
        if "s" in mn: return (384, 384)
        if "m" in mn or "l" in mn: return (480, 480)
        return (224, 224)

    # Inception / Xception
    if any(x in mn for x in ["inception", "xception"]):
        return (299, 299)

    # NASNet
    if "nasnetlarge" in mn:
        return (331, 331)

    return (224, 224)

# ======================================================
# DATA PIPELINE
# ======================================================
def build_dataframe(dataset_dir):
    data = []
    for cls in sorted(os.listdir(dataset_dir)):
        class_dir = os.path.join(dataset_dir, cls)
        if not os.path.isdir(class_dir): continue
        for f in os.listdir(class_dir):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                data.append([os.path.join(class_dir, f), cls])
    df = pd.DataFrame(data, columns=["filepath", "label"])
    df["label_id"] = df["label"].apply(lambda x: 1 if "pneu" in x.lower() else 0).astype(int)
    return df

def create_tf_datasets_from_indices(images, labels, tr_idx, va_idx, img_size, batch_size):
    def _load_image(path, label):
        img = tf.io.read_file(path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, img_size)
        img = tf.cast(img, tf.float32) / 255.0
        return img, tf.cast(label, tf.float32)

    def _augment(img, label):
        img = tf.image.random_flip_left_right(img)
        img = tf.image.random_brightness(img, 0.05)
        return img, label

    train_ds = tf.data.Dataset.from_tensor_slices((images[tr_idx], labels[tr_idx]))
    train_ds = train_ds.map(_load_image, num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.shuffle(512).map(_augment, num_parallel_calls=AUTOTUNE).batch(batch_size).prefetch(AUTOTUNE)

    val_ds = tf.data.Dataset.from_tensor_slices((images[va_idx], labels[va_idx]))
    val_ds = val_ds.map(_load_image, num_parallel_calls=AUTOTUNE).batch(batch_size).prefetch(AUTOTUNE)

    return train_ds, val_ds

# ======================================================
# MODELING
# ======================================================
def build_cnn_model(architecture, img_size):
    try:
        norm_arch = architecture.replace(" ", "").lower()
        # Find the correct casing from Keras Applications
        import tensorflow as tf
        all_apps = [name for name in dir(tf.keras.applications) if not name.startswith('_')]

        target_name = None
        for name in all_apps:
            if name.lower() == norm_arch:
                target_name = name
                break

        if target_name and hasattr(tf.keras.applications, target_name):
            model_fn = getattr(tf.keras.applications, target_name)
        else:
            print(f"Aviso: Arquitectura '{architecture}' no detectada en Keras. Usando MobileNetV2.")
            model_fn = MobileNetV2

        base = model_fn(weights="imagenet", include_top=False, input_shape=(*img_size, 3))
        base.trainable = False
    except Exception as e:
        print(f"Error crítico cargando {architecture}: {str(e)}. Fallback a MobileNetV2.")
        base = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        base.trainable = False

    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs=base.input, outputs=outputs)
    model.compile(optimizer=Adam(1e-4), loss="binary_crossentropy", metrics=["accuracy"])
    return model

# ======================================================
# DATABASE CALLBACK
# ======================================================
class DBProgressCallback(Callback):
    def __init__(self, job_id, total_epochs):
        super().__init__()
        self.job_id = job_id
        self.total_epochs = total_epochs
        self.metrics_history = []
        self.current_epoch_global = 0

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.current_epoch_global += 1
        current_metrics = {
            "epoch": self.current_epoch_global,
            "loss": float(logs.get("loss", 0)),
            "accuracy": float(logs.get("accuracy", 0)),
            "val_loss": float(logs.get("val_loss", 0)),
            "val_accuracy": float(logs.get("val_accuracy", 0)),
        }
        self.metrics_history.append(current_metrics)

        progress = round((self.current_epoch_global / self.total_epochs) * 100, 2)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE training_jobs
            SET progress = %s, metrics_json = %s
            WHERE id = %s
        """, (progress, json.dumps(self.metrics_history), self.job_id))
        conn.commit()
        conn.close()

# ======================================================
# BACKGROUND RUNNER
# ======================================================
def run_training_job_sync(job_id: int, dataset_path: str, model_name: str, batch_size: int = 32, epochs: int = 10, n_splits: int = 1, seed: int = 42):
    try:
        import numpy as np
        from sklearn.model_selection import StratifiedKFold

        if not os.path.exists(dataset_path):
            raise ValueError(f"Directorio de dataset no encontrado: {dataset_path}")

        img_size = get_img_size(model_name)
        df = build_dataframe(dataset_path)
        if len(df) == 0:
            raise ValueError("No se encontraron imágenes en el directorio.")

        images = df["filepath"].values
        labels = df["label_id"].values

        total_epochs = epochs * max(1, n_splits)
        db_callback = DBProgressCallback(job_id=job_id, total_epochs=total_epochs)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE training_jobs SET status = 'In Progress', progress = 0 WHERE id = %s", (job_id,))
        conn.commit()
        conn.close()

        if n_splits > 1:
            skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
            folds = list(skf.split(images, labels))
        else:
            indices = np.arange(len(images))
            np.random.seed(seed)
            np.random.shuffle(indices)
            split = int(0.8 * len(images))
            folds = [(indices[:split], indices[split:])]

        for current_fold, (tr_idx, va_idx) in enumerate(folds, 1):
            train_ds, val_ds = create_tf_datasets_from_indices(images, labels, tr_idx, va_idx, img_size, batch_size)
            model = build_cnn_model(model_name, img_size)
            model.fit(
                train_ds,
                validation_data=val_ds,
                epochs=epochs,
                callbacks=[db_callback],
                verbose=0
            )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE training_jobs
            SET status = 'Completed', progress = 100.0, finished_at = %s
            WHERE id = %s
        """, (datetime.now(), job_id))
        conn.commit()
        conn.close()

    except Exception as e:
        error_info = traceback.format_exc()
        print(f"Error en entrenamiento job {job_id}: {error_info}")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE training_jobs SET status = 'Failed', progress = 0.0 WHERE id = %s", (job_id,))
            conn.commit()
            conn.close()
        except:
            pass
