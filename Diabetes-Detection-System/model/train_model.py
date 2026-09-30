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
    
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Identify columns where 0 is invalid/missing physiological data
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
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=8, 
        random_state=42, 
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)
    
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
