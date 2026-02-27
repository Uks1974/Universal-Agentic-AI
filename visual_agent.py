# visual_agent.py

import matplotlib.pyplot as plt
import pandas as pd
import os

OUTPUT_DIR = "generated_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_basic_graph(data):
    """
    Generates a simple chart if numeric data is available.
    Returns image path or None.
    """
    if not hasattr(data, "select_dtypes"):
        return None

    numeric_cols = data.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    col = numeric_cols[0]

    plt.figure(figsize=(6, 4))
    data[col].plot(title=f"Trend of {col}")
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "key_trend.png")
    plt.savefig(path)
    plt.close()

    return path