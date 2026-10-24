import os
import datetime
import pandas as pd
import numpy as np
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

def run_pipeline():
    print("Iniciando Pipeline de Machine Learning...")
    
    # Carga del dataset
    dataset_id = "scikit-learn/auto-mpg"
    hf_ds = load_dataset(dataset_id, split="train")
    df = pd.DataFrame(hf_ds)
    
    # Estandarizar columnas
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # Reemplazar '?' por NaN y convertir a numericas
    df = df.replace('?', np.nan)
    num_cols = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'mpg']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    num_features = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year']
    cat_features = ['origin']
    
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), cat_features)
    ])
    
    # 1. Regresion Lineal
    cols_to_drop_reg = [c for c in ['mpg', 'car_name'] if c in df.columns]
    X_reg = df.drop(columns=cols_to_drop_reg)
    y_reg = df['mpg']
    
    X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    reg_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    reg_pipeline.fit(X_tr_r, y_tr_r)
    y_pred_r = reg_pipeline.predict(X_te_r)
    
    mae_r = mean_absolute_error(y_te_r, y_pred_r)
    rmse_r = np.sqrt(mean_squared_error(y_te_r, y_pred_r))
    r2_r = r2_score(y_te_r, y_pred_r)
    
    # 2. Clasificacion
    def categorizar(v):
        if v <= 19.0: return 'Baja'
        elif v <= 29.0: return 'Media'
        else: return 'Alta'
        
    df['eficiencia_combustible'] = df['mpg'].apply(categorizar)
    
    cols_to_drop_cls = [c for c in ['mpg', 'car_name', 'eficiencia_combustible'] if c in df.columns]
    X_cls = df.drop(columns=cols_to_drop_cls)
    y_cls = df['eficiencia_combustible']
    
    X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls)
    
    cls_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])
    cls_pipeline.fit(X_tr_c, y_tr_c)
    y_pred_c = cls_pipeline.predict(X_te_c)
    
    acc_c = accuracy_score(y_te_c, y_pred_c)
    prec_c = precision_score(y_te_c, y_pred_c, average='weighted')
    rec_c = recall_score(y_te_c, y_pred_c, average='weighted')
    f1_c = f1_score(y_te_c, y_pred_c, average='weighted')
    cm_c = confusion_matrix(y_te_c, y_pred_c, labels=['Baja', 'Media', 'Alta'])
    
    # 3. Guardar .txt
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_content = f"""======================================================================
RESUMEN AUTOMÁTICO DE EJECUCIÓN DE MODELOS DE MACHINE LEARNING
Fecha de ejecución: {now_str}
======================================================================

1. DATASET Y PREPROCESAMIENTO
- Dataset: scikit-learn/auto-mpg (Hugging Face)
- Registros: {df.shape[0]} | Columnas: {df.shape[1]}
- Preprocesamiento: Conversión de '?' a NaN, Imputación por mediana en horsepower,
  StandardScaler en numéricas y OneHotEncoder en origin. Sin Data Leakage.

2. MODELO DE REGRESIÓN LINEAL (Objetivo: mpg)
- MAE:  {mae_r:.4f} mpg
- RMSE: {rmse_r:.4f} mpg
- R²:   {r2_r:.4f}

3. MODELO DE CLASIFICACIÓN (Objetivo: eficiencia_combustible [Baja/Media/Alta])
- Accuracy:  {acc_c:.4f}
- Precision: {prec_c:.4f}
- Recall:    {rec_c:.4f}
- F1-Score:  {f1_c:.4f}
- Matriz de Confusión [Baja, Media, Alta]:
{cm_c}
======================================================================
"""
    with open("resumen_modelos.txt", "w", encoding="utf-8") as f:
        f.write(txt_content)
        
    print("\n¡Pipeline ejecutado exitosamente! Se generó 'resumen_modelos.txt'.")

if __name__ == "__main__":
    run_pipeline()