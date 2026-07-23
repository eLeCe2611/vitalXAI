"""
5_evaluate_delong.py (VERSIÓN MLOPS)
====================================
Aplica el Test Estadístico de DeLong a la Validación Externa.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
import seaborn as sns

# ======================================================
# CONFIGURACIÓN DINÁMICA WEB
# ======================================================
SESSION_ID = os.getenv("TFG_SESSION_ID")

if not SESSION_ID:
    print("[ERROR] No se ha proporcionado un ID de sesión.")
    sys.exit(1)

SESSION_DIR = f"training_results/{SESSION_ID}/external_validation"
INPUT_FILE = f"{SESSION_DIR}/external_raw_probabilities.csv"
P_VALUE_THRESHOLD = 0.05

def compute_midrank(x):
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1)
        i = j
    T2 = np.empty(N, dtype=float)
    T2[J] = T + 1
    return T2

def compute_delong_cov(y_true, preds_a, preds_b):
    idx_1, idx_0 = y_true == 1, y_true == 0
    m, n = np.sum(idx_1), np.sum(idx_0)

    tz1_a, tz0_a, tz_a = compute_midrank(preds_a[idx_1]), compute_midrank(preds_a[idx_0]), compute_midrank(preds_a)
    v10_a, v01_a = (tz_a[idx_1] - tz1_a) / n, 1 - (tz_a[idx_0] - tz0_a) / m

    tz1_b, tz0_b, tz_b = compute_midrank(preds_b[idx_1]), compute_midrank(preds_b[idx_0]), compute_midrank(preds_b)
    v10_b, v01_b = (tz_b[idx_1] - tz1_b) / n, 1 - (tz_b[idx_0] - tz0_b) / m

    s10, s01 = np.cov(v10_a, v10_b), np.cov(v01_a, v01_b)
    return s10 / m + s01 / n

def delong_roc_test(y_true, preds_a, preds_b):
    auc_a = scipy.stats.mannwhitneyu(preds_a[y_true == 1], preds_a[y_true == 0], alternative='greater').statistic / (np.sum(y_true == 1) * np.sum(y_true == 0))
    auc_b = scipy.stats.mannwhitneyu(preds_b[y_true == 1], preds_b[y_true == 0], alternative='greater').statistic / (np.sum(y_true == 1) * np.sum(y_true == 0))
    diff = auc_a - auc_b
    cov = compute_delong_cov(y_true, preds_a, preds_b)
    var = cov[0, 0] + cov[1, 1] - 2 * cov[0, 1]
    if var == 0: return 1.0
    z = diff / np.sqrt(var)
    return 2 * scipy.stats.norm.sf(abs(z))

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encontró el archivo de probabilidades. Ejecuta la validación primero.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    y_true = df["y_true"].values

    model_cols = [c for c in df.columns if c.startswith("prob_")]
    models = [c.replace("prob_", "") for c in model_cols]

    if len(models) < 2:
        print("[AVISO] Solo hay 1 modelo evaluado. Se omite el test de DeLong (se necesitan 2 o más).")
        sys.exit(0)

    n = len(models)
    p_matrix = pd.DataFrame(np.ones((n, n)), index=models, columns=models)

    for i in range(n):
        for j in range(i + 1, n):
            p_val = delong_roc_test(y_true, df[f"prob_{models[i]}"].values, df[f"prob_{models[j]}"].values)
            p_matrix.loc[models[i], models[j]] = p_matrix.loc[models[j], models[i]] = p_val

    p_matrix.to_csv(os.path.join(SESSION_DIR, "delong_pvalues_matrix.csv"))

    plt.figure(figsize=(8, 6))
    sns.heatmap(p_matrix, annot=True, cmap="coolwarm", vmin=0, vmax=0.1, cbar_kws={'label': 'p-value'}, annot_kws={"size": 10}, fmt=".3f")
    plt.title(f"Test de DeLong p-values (Validación Externa)\n< {P_VALUE_THRESHOLD} es Estadísticamente Significativo")
    plt.tight_layout()
    plt.savefig(os.path.join(SESSION_DIR, "delong_heatmap.png"), dpi=300)
    plt.close()
    print("\n[DELONG COMPLETADO]")

if __name__ == "__main__":
    main()
