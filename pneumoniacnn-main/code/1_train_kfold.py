"""
train_kfold.py
==============
CNN training and predictive performance evaluation using
5-fold stratified cross-validation with class-balanced undersampling.
"""

import os
import random
import sys

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

# ======================================================
# CONFIGURACIÓN DINÁMICA (ESTRICTA - CONECTADA A LA WEB)
# ======================================================
DATASET_DIR = os.getenv("TFG_DATASET_DIR")
SESSION_ID = os.getenv("TFG_SESSION_ID")

if not DATASET_DIR or not os.path.exists(DATASET_DIR) or not SESSION_ID:
    print(f"\n[ERROR CRÍTICO] Faltan variables de entorno (Dataset o Session ID).")
    sys.exit(1)

MODEL_NAME = os.getenv("TFG_MODEL_NAME", "DenseNet121")
OUTPUT_DIR = f"training_results/{SESSION_ID}/{MODEL_NAME}"

# Asignación dinámica del tamaño de imagen según la arquitectura elegida
if MODEL_NAME == "NASNetLarge":
    IMG_SIZE = (331, 331)
elif MODEL_NAME in ["InceptionV3", "Xception", "InceptionResNetV2"]:
    IMG_SIZE = (299, 299)
else:
    IMG_SIZE = (224, 224)

BATCH_SIZE = int(os.getenv("TFG_BATCH_SIZE", "32"))
EPOCHS     = int(os.getenv("TFG_EPOCHS", "25"))
LEARNING_RATE = float(os.getenv("TFG_LEARNING_RATE", "0.001"))

N_SPLITS = 5
SEED = 42

os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Dataset validado en: {DATASET_DIR}")
print(f"Iniciando sesión {SESSION_ID} -> Modelo: {MODEL_NAME}")

# ======================================================
# REPRODUCIBILIDAD Y PIPELINE
# ======================================================
tf.random.set_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)
AUTOTUNE = tf.data.AUTOTUNE

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

def _load_image(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, IMG_SIZE)
    img = tf.cast(img, tf.float32) / 255.0
    return img, tf.cast(label, tf.float32)

def augment_fn(img, label):
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_brightness(img, 0.05)
    img = tf.image.random_contrast(img, 0.9, 1.1)
    return img, label

def build_dataset(paths, labels, train=True):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    ds = ds.map(_load_image, num_parallel_calls=AUTOTUNE)
    if train:
        ds = ds.shuffle(512, seed=SEED).map(augment_fn, num_parallel_calls=AUTOTUNE)
    return ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)

# ======================================================
# CONSTRUCCIÓN DEL MODELO (DINÁMICA)
# ======================================================
def build_model(architecture="ResNet50", lr=1e-4):
    print(f"Construyendo modelo: {architecture} con tamaño de entrada {IMG_SIZE}")
    strategy = tf.distribute.get_strategy()
    with strategy.scope():

        # Magia de Python: Carga cualquier modelo de tf.keras.applications por su nombre de texto
        try:
            model_class = getattr(tf.keras.applications, architecture)
        except AttributeError as err:
            raise ValueError(f"Error: La arquitectura '{architecture}' no existe en TensorFlow Keras Applications.") from err

        base = model_class(weights="imagenet", include_top=False, input_shape=(*IMG_SIZE,3))
        base.trainable = False

        x = layers.GlobalAveragePooling2D()(base.output)
        x = layers.Dense(512, activation="relu")(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(256, activation="relu")(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(1, activation="sigmoid")(x)

        model = models.Model(inputs=base.input, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=lr), loss="binary_crossentropy", metrics=["accuracy"])
    return model

# ======================================================
# ENTRENAMIENTO PRINCIPAL
# ======================================================
def main():
    df = build_dataframe(DATASET_DIR)
    image_paths, labels = df["filepath"].values, df["label_id"].values
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    results = []

    for fold, (tr, va) in enumerate(skf.split(image_paths, labels), 1):
        print(f"\n===== FOLD {fold} =====")
        y_tr = labels[tr]
        idx0, idx1 = tr[y_tr == 0], tr[y_tr == 1]
        n = min(len(idx0), len(idx1))

        balanced_idx = np.concatenate([
            np.random.choice(idx0, n, replace=False),
            np.random.choice(idx1, n, replace=False)
        ])
        np.random.shuffle(balanced_idx)

        train_ds = build_dataset(image_paths[balanced_idx], labels[balanced_idx], True)
        val_ds   = build_dataset(image_paths[va], labels[va], False)

        model = build_model(architecture=MODEL_NAME, lr=LEARNING_RATE)
        ckpt = f"{OUTPUT_DIR}/best_fold{fold}.keras"

        callbacks = [
            ModelCheckpoint(ckpt, save_best_only=True, monitor="val_loss"),
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=1e-6, verbose=1)
        ]

        model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks, verbose=1)

        y_true = np.concatenate([y.numpy() for _, y in val_ds])
        y_prob = np.concatenate([model.predict(x).ravel() for x, _ in val_ds])
        y_pred = (y_prob >= 0.5).astype(int)

        results.append({
            "fold": fold, "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred), "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred), "auc": roc_auc_score(y_true, y_prob)
        })

        pd.DataFrame({"filepath": image_paths[va], "y_true": y_true, "y_prob": y_prob, "y_pred": y_pred}).to_csv(f"{OUTPUT_DIR}/predictions_fold{fold}.csv", index=False)

    df_res = pd.DataFrame(results)
    df_res.loc["mean"] = df_res.mean()
    df_res.loc["std"]  = df_res.std()

    df_res["fold"] = df_res["fold"].astype(str)
    df_res.at["mean", "fold"] = "Media"
    df_res.at["std", "fold"] = "Std"

    df_res.to_csv(f"{OUTPUT_DIR}/kfold_results.csv", index=False)

    print("\n===== FINAL SUMMARY =====")
    print(df_res)

if __name__ == "__main__":
    main()
