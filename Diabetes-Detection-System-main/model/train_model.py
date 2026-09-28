# ==============================================================================
# DIABETES DETECTION SYSTEM — MACHINE LEARNING TRAINING PIPELINE
# ==============================================================================
# Trains Random Forest Classifier on Pima Indians Diabetes Dataset.
# Aa script Pima Indians dataset load karse, missing zero values clean karse,
# StandardScaler fit karse ane Random Forest ML model train kari pickle file save karse.
# ==============================================================================

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

def train_and_save_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'diabetes.csv')
    model_dir = os.path.join(base_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    # --------------------------------------------------------------------------
    # 1. LOAD DATASET & DATA CLEANING / IMPUTATION
    # CSV file read karse. Glucose, BP vagere ma 0 values invalid hoy,
    # tethi 0 ne column median value sathe replace/fill karva ma aave chhe.
    # --------------------------------------------------------------------------
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in zero_columns:
        df[col] = df[col].replace(0, np.nan)
        col_median = df[col].median()
        df[col].fillna(col_median, inplace=True)
        
    feature_cols = [
        'Pregnancies', 'Glucose', 'BloodPressure', 
        'SkinThickness', 'Insulin', 'BMI', 
        'DiabetesPedigreeFunction', 'Age'
    ]
    
    X = df[feature_cols]
    y = df['Outcome']
    
    # --------------------------------------------------------------------------
    # 2. TRAIN-TEST SPLIT (80% Training, 20% Evaluation)
    # Data ne Train (80%) ane Test (20%) ma divide karie chhe.
    # --------------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # --------------------------------------------------------------------------
    # 3. FEATURE SCALING (StandardScaler)
    # Features nuy scale same karva mate StandardScaler transform thase.
    # --------------------------------------------------------------------------
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # --------------------------------------------------------------------------
    # 4. RANDOM FOREST CLASSIFIER MODEL FITTING
    # 150 Decision Trees sathe Random Forest Classifier train karie chhe.
    # --------------------------------------------------------------------------
    model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=8, 
        random_state=42, 
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)
    
    # --------------------------------------------------------------------------
    # 5. MODEL EVALUATION & METRICS PRINT
    # Accuracy ane ROC-AUC Score calculate karse.
    # --------------------------------------------------------------------------
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print("=" * 50)
    print("MODEL TRAINING COMPLETE")
    print(f"Accuracy: {acc * 100:.2f}%")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("=" * 50)
    
    # --------------------------------------------------------------------------
    # 6. SAVE MODEL & SCALER BINARIES (.pkl)
    # Trained model ane scaler pkl files ma save thai jase.
    # --------------------------------------------------------------------------
    model_path = os.path.join(model_dir, 'diabetes_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Saved model to: {model_path}")
    print(f"Saved scaler to: {scaler_path}")

if __name__ == '__main__':
    train_and_save_model()
