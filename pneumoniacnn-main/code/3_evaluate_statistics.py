"""
evaluate_statistics.py (VERSIÓN MLOPS)
======================================
Genera tabla comparativa y Test de Wilcoxon dinámicamente 
para los modelos dentro de una sesión específica de la web.
"""

import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import seaborn as sns
import matplotlib.pyplot as plt

# ======================================================
# CONFIGURACIÓN DINÁMICA WEB
# ======================================================
SESSION_ID = os.getenv("TFG_SESSION_ID")

if not SESSION_ID:
    print("[ERROR] No se ha proporcionado un ID de sesión.")
    sys.exit(1)

SESSION_DIR = f"training_results/{SESSION_ID}"
if not os.path.exists(SESSION_DIR):
    print(f"[ERROR] La carpeta de la sesión no existe: {SESSION_DIR}")
    sys.exit(1)

TARGET_METRIC = "auc" # Métrica a comparar
P_VALUE_THRESHOLD = 0.05

def get_models_in_session():
    """Detecta automáticamente qué modelos se entrenaron en esta sesión."""
    models = []
    for item in os.listdir(SESSION_DIR):
        item_path = os.path.join(SESSION_DIR, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "kfold_results.csv")):
            models.append(item)
    return models

def load_fold_results(models):
    all_results = {}
    for model in models:
        path = os.path.join(SESSION_DIR, model, "kfold_results.csv")
        df = pd.read_csv(path)
        # Extraer solo Folds numéricos (ignorar Media y Std)
        folds_df = df[df['fold'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]
        all_results[model] = folds_df[TARGET_METRIC].astype(float).values
    return all_results

def main():
    models = get_models_in_session()
    
    # CORRECCIÓN: Ahora pide mínimo 1 modelo para funcionar en lugar de 2
    if len(models) < 1:
        print("[AVISO] No hay modelos terminados en esta sesión para evaluar.")
        sys.exit(0)

    results = load_fold_results(models)

    # 1. Tabla Resumen (SE CREA SIEMPRE, INCLUSO CON 1 SOLO MODELO)
    summary = []
    for model, values in results.items():
        summary.append({"Model": model, "Mean": np.mean(values), "Std": np.std(values)})
    
    df_summary = pd.DataFrame(summary).sort_values(by="Mean", ascending=False)
    df_summary.to_csv(os.path.join(SESSION_DIR, "session_ranking.csv"), index=False)

    # 2. Matriz Wilcoxon (SOLO SE CALCULA SI HAY 2 O MÁS MODELOS)
    if len(models) >= 2:
        n = len(models)
        p_matrix = pd.DataFrame(np.ones((n, n)), index=models, columns=models)
        
        for i in range(n):
            for j in range(i+1, n):
                data_a, data_b = results[models[i]], results[models[j]]
                if np.array_equal(data_a, data_b):
                    p_val = 1.0
                else:
                    try:
                        stat, p_val = wilcoxon(data_a, data_b)
                    except ValueError:
                        p_val = 1.0
                p_matrix.loc[models[i], models[j]] = p_val
                p_matrix.loc[models[j], models[i]] = p_val

        p_matrix.to_csv(os.path.join(SESSION_DIR, "wilcoxon_matrix.csv"))

        # Mapa de Calor (Heatmap)
        plt.figure(figsize=(8, 6))
        ax = sns.heatmap(p_matrix, annot=True, cmap="coolwarm", vmin=0, vmax=0.1, 
                         cbar_kws={'label': 'p-value'}, annot_kws={"size": 10})
        plt.title(f"Test de Wilcoxon ({TARGET_METRIC.upper()})\n< {P_VALUE_THRESHOLD} es Estadísticamente Significativo")
        plt.tight_layout()
        plt.savefig(os.path.join(SESSION_DIR, "wilcoxon_heatmap.png"), dpi=300)
        plt.close()

        print("[ÉXITO] Ranking y Matriz de Wilcoxon generados correctamente.")
    else:
        print("[ÉXITO] Ranking generado. Se omiten las estadísticas de Wilcoxon (se necesitan al menos 2 modelos).")

if __name__ == "__main__":
    main()