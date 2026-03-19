# ============================================================================
# SECTION 1: Load and Prepare Data
# ============================================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import json
import os
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MACHINE LEARNING MODEL DEVELOPMENT")
print("="*80)

# Load the cleaned dataset
df = pd.read_csv('data/real_state_clean.csv')
print(f"\nDataset loaded: {df.shape}")
print(f"Features: {df.columns.tolist()}")

# ============================================================================
# SECTION 2: Feature Engineering
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: Feature Engineering")
print("="*80)

# Select features for the model
X = df[['Provincia', 'Lugar_Normalizado', 'Num. dormitorios', 'Num. banos', 'Area', 'Num. garages']].copy()
y = df['Precio'].copy()

print(f"\nInput features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"\nFeatures: {X.columns.tolist()}")

# Encode categorical variables
print("\nEncoding categorical variables...")
le_provincia = LabelEncoder()
le_lugar = LabelEncoder()

X['Provincia'] = le_provincia.fit_transform(X['Provincia'])
X['Lugar_Normalizado'] = le_lugar.fit_transform(X['Lugar_Normalizado'])

print(f"✓ Provincia encoded: {len(le_provincia.classes_)} unique values")
print(f"✓ Lugar_Normalizado encoded: {len(le_lugar.classes_)} unique values")

# Scale numeric features
print("\nScaling numeric features...")
scaler = StandardScaler()
numeric_features = ['Num. dormitorios', 'Num. banos', 'Area', 'Num. garages']
X[numeric_features] = scaler.fit_transform(X[numeric_features])
print("✓ Features scaled")

# ============================================================================
# SECTION 3: Train-Test Split
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: Train-Test Split")
print("="*80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")
print(f"Training split: {len(X_train) / len(X) * 100:.1f}%")
print(f"Testing split: {len(X_test) / len(X) * 100:.1f}%")

# ============================================================================
# SECTION 4: Model Training and Evaluation
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: Model Training and Evaluation")
print("="*80)

models = {}

# Linear Regression
print("\n" + "-"*50)
print("1. Linear Regression")
print("-"*50)
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
mae_lr = mean_absolute_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"RMSE: ${rmse_lr:.2f}")
print(f"MAE:  ${mae_lr:.2f}")
print(f"R²:   {r2_lr:.4f}")

models['Linear Regression'] = {
    'model': lr_model,
    'r2': r2_lr,
    'rmse': rmse_lr,
    'mae': mae_lr
}

# Random Forest Regressor
print("\n" + "-"*50)
print("2. Random Forest Regressor")
print("-"*50)
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"RMSE: ${rmse_rf:.2f}")
print(f"MAE:  ${mae_rf:.2f}")
print(f"R²:   {r2_rf:.4f}")

models['Random Forest'] = {
    'model': rf_model,
    'r2': r2_rf,
    'rmse': rmse_rf,
    'mae': mae_rf
}

# ============================================================================
# SECTION 5: Model Comparison and Selection
# ============================================================================
print("\n" + "="*80)
print("SECTION 5: Model Comparison and Selection")
print("="*80)

print("\nModel Performance Summary:")
print("-"*50)
for model_name, metrics in models.items():
    print(f"\n{model_name}:")
    print(f"  R² Score:  {metrics['r2']:.4f}")
    print(f"  RMSE:      ${metrics['rmse']:.2f}")
    print(f"  MAE:       ${metrics['mae']:.2f}")

# Select best model based on R²
best_model_name = max(models, key=lambda x: models[x]['r2'])
best_model = models[best_model_name]['model']
best_metrics = models[best_model_name]

print(f"\n✓ Selected Model: {best_model_name}")
print(f"  R² Score:  {best_metrics['r2']:.4f}")
print(f"  RMSE:      ${best_metrics['rmse']:.2f}")
print(f"  MAE:       ${best_metrics['mae']:.2f}")

# Feature importance (if available)
if hasattr(best_model, 'feature_importances_'):
    print(f"\nFeature Importance ({best_model_name}):")
    feature_names = X.columns
    importances = best_model.feature_importances_
    
    # Sort by importance
    indices = np.argsort(importances)[::-1]
    
    for i, idx in enumerate(indices[:len(feature_names)]):
        print(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")

# ============================================================================
# SECTION 6: Save Model and Encoders
# ============================================================================
print("\n" + "="*80)
print("SECTION 6: Save Model and Encoders")
print("="*80)

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save the model
model_path = 'models/rental_price_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"✓ Model saved to '{model_path}'")

# Save the encoders
provincia_encoder_path = 'models/provincia_encoder.pkl'
with open(provincia_encoder_path, 'wb') as f:
    pickle.dump(le_provincia, f)
print(f"✓ Provincia encoder saved to '{provincia_encoder_path}'")

lugar_encoder_path = 'models/lugar_encoder.pkl'
with open(lugar_encoder_path, 'wb') as f:
    pickle.dump(le_lugar, f)
print(f"✓ Lugar encoder saved to '{lugar_encoder_path}'")

# Save the scaler
scaler_path = 'models/scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"✓ Scaler saved to '{scaler_path}'")

# Save metadata
metadata = {
    'model_type': best_model_name,
    'model_path': model_path,
    'r2_score': float(best_metrics['r2']),
    'rmse': float(best_metrics['rmse']),
    'mae': float(best_metrics['mae']),
    'features': X.columns.tolist(),
    'numeric_features': numeric_features,
    'provincias': le_provincia.classes_.tolist(),
    'lugares': le_lugar.classes_.tolist(),
    'scaler_path': scaler_path,
    'provincia_encoder_path': provincia_encoder_path,
    'lugar_encoder_path': lugar_encoder_path
}

metadata_path = 'models/metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Metadata saved to '{metadata_path}'")

print("\n" + "="*80)
print("✓ TRAINING COMPLETE")
print("="*80)
print(f"\nYour model is ready for deployment!")
print(f"Model type: {best_model_name}")
print(f"Performance: R² = {best_metrics['r2']:.4f}, RMSE = ${best_metrics['rmse']:.2f}")
