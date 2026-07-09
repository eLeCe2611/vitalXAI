"""
2_train_transformer_kfold.py
==========================
Entrenamiento avanzado de Transformers usando 5-fold CV en la plataforma MLOps.
"""

import os
# --- CONFIGURACIÓN ESTRICTA PARA HUGGING FACE Y TENSORFLOW ---
os.environ["TF_USE_LEGACY_KERAS"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USE_TF"] = "1" # <--- ESTO OBLIGA A HUGGING FACE A MOSTRAR LAS CLASES TF
# -------------------------------------------------------------

import sys
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from tf_keras.optimizers import AdamW
from tf_keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tf_keras.losses import BinaryCrossentropy
from transformers import TFAutoModelForImageClassification

# ======================================================
# CONFIGURACIÓN DINÁMICA WEB
# ======================================================
DATASET_DIR = os.getenv("TFG_DATASET_DIR")
SESSION_ID = os.getenv("TFG_SESSION_ID") 

if not DATASET_DIR or not SESSION_ID:
    print(f"\n[ERROR CRÍTICO] Faltan variables de entorno.")
    sys.exit(1)

MODEL_NAME = os.getenv("TFG_MODEL_NAME", "swin_base") 
OUTPUT_DIR = f"training_results/{SESSION_ID}/{MODEL_NAME}"

HF_MODEL_IDS = {
    "deit": "facebook/deit-base-distilled-patch16-224",
    "swin_base": "microsoft/swin-base-patch4-window7-224",
    "vit_384": "google/vit-base-patch16-384"
}

IMG_SIZE = (384, 384) if MODEL_NAME == "vit_384" else (224, 224)

BATCH_SIZE = int(os.getenv("TFG_BATCH_SIZE", "16"))
EPOCHS     = int(os.getenv("TFG_EPOCHS", "25"))
USER_LR    = float(os.getenv("TFG_LEARNING_RATE", "0.001"))
SAFE_LR    = 5e-5 if USER_LR >= 0.001 else USER_LR

N_SPLITS = 5
SEED = 42

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================================================
# REPRODUCIBILIDAD Y PIPELINE
# ======================================================
tf.random.set_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)
AUTOTUNE = tf.data.AUTOTUNE

def build_dataframe(dataset_dir):
    data = []
    for cls in ["NORMAL", "PNEUMONIA"]:
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
    return {"pixel_values": img}, tf.cast(label, tf.float32)

def augment_fn(inputs, label):
    img = inputs["pixel_values"]
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_brightness(img, 0.05)
    img = tf.image.random_contrast(img, 0.9, 1.1)
    return {"pixel_values": img}, label

def format_for_hf(inputs, label):
    img = inputs["pixel_values"]
    if MODEL_NAME in ["deit", "vit_384", "swin_base"]:
        img = tf.transpose(img, [2, 0, 1])
    return {"pixel_values": img}, label

def build_dataset(paths, labels, train=True):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    ds = ds.map(_load_image, num_parallel_calls=AUTOTUNE)
    if train: ds = ds.shuffle(512, seed=SEED).map(augment_fn, num_parallel_calls=AUTOTUNE)
    ds = ds.map(format_for_hf, num_parallel_calls=AUTOTUNE)
    return ds.batch(BATCH_SIZE, drop_remainder=True).prefetch(AUTOTUNE)

def build_hf_model(architecture, lr):
    model_id = HF_MODEL_IDS[architecture]
    strategy = tf.distribute.get_strategy()
    with strategy.scope():
        model = TFAutoModelForImageClassification.from_pretrained(model_id, num_labels=1, ignore_mismatched_sizes=True)
        model.compile(
            optimizer=AdamW(learning_rate=lr, weight_decay=1e-4),
            loss=BinaryCrossentropy(from_logits=True),
            metrics=["accuracy"],
            run_eagerly=(architecture == "swin_base")
        )
    return model

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

        balanced_idx = np.concatenate([np.random.choice(idx0, n, replace=False), np.random.choice(idx1, n, replace=False)])
        np.random.shuffle(balanced_idx)

        train_ds = build_dataset(image_paths[balanced_idx], labels[balanced_idx], True)
        val_ds   = build_dataset(image_paths[va], labels[va], False)
        
        model = build_hf_model(architecture=MODEL_NAME, lr=SAFE_LR)
        ckpt = f"{OUTPUT_DIR}/best_fold{fold}.weights.h5"
        
        callbacks = [
            ModelCheckpoint(filepath=ckpt, save_weights_only=True, monitor='val_loss', mode='min', save_best_only=True),
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
        ]

        model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks, verbose=1)

        y_true = np.concatenate([y.numpy() for _, y in val_ds])
        predictions = model.predict(val_ds)
        y_prob = tf.nn.sigmoid(predictions.logits).numpy().ravel()
        y_pred = (y_prob >= 0.5).astype(int)

        results.append({
            "fold": fold, "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred), "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred), "auc": roc_auc_score(y_true, y_prob)
        })

        valid_length = len(y_prob)
        val_filepaths = image_paths[va][:valid_length]

        pd.DataFrame({"filepath": val_filepaths, "y_true": y_true, "y_prob": y_prob, "y_pred": y_pred}).to_csv(f"{OUTPUT_DIR}/predictions_fold{fold}.csv", index=False)

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