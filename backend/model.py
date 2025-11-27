import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os

print("\n" + "="*60)
print("🏠 House Price Prediction Model Training")
print("="*60)

# Create sample dataset (replace with your actual dataset)
print("\n📊 Creating sample dataset...")
np.random.seed(42)
n_samples = 1000

data = {
    'sqft': np.random.randint(800, 4000, n_samples),
    'bedrooms': np.random.randint(1, 6, n_samples),
    'bathrooms': np.random.randint(1, 4, n_samples),
    'age': np.random.randint(0, 50, n_samples),
    'location': np.random.choice([0, 1, 2], n_samples)  # 0=rural, 1=suburban, 2=urban
}

# Create realistic price based on features
data['price'] = (
    data['sqft'] * np.where(data['location'] == 2, 200, np.where(data['location'] == 1, 150, 100)) +
    data['bedrooms'] * 15000 +
    data['bathrooms'] * 10000 -
    data['age'] * 2000 +
    np.random.normal(0, 20000, n_samples)  # Add some noise
)

df = pd.DataFrame(data)

# Save dataset
os.makedirs('data', exist_ok=True)
df.to_csv('data/house_data.csv', index=False)
print(f"✓ Dataset created with {len(df)} samples")
print(f"✓ Dataset saved to: data/house_data.csv")

# Prepare features and target
X = df[['sqft', 'bedrooms', 'bathrooms', 'age', 'location']]
y = df['price']

print("\n📈 Dataset Statistics:")
print(f"   Average Price: ${y.mean():,.2f}")
print(f"   Min Price: ${y.min():,.2f}")
print(f"   Max Price: ${y.max():,.2f}")
print(f"   Std Dev: ${y.std():,.2f}")

# Split data
print("\n🔀 Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✓ Training samples: {len(X_train)}")
print(f"✓ Testing samples: {len(X_test)}")

# Train model
print("\n🤖 Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)
print("✓ Model trained successfully!")

# Evaluate model
print("\n📊 Model Evaluation:")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)
train_mse = mean_squared_error(y_train, y_pred_train)
test_mse = mean_squared_error(y_test, y_pred_test)
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)

print(f"\n   Training Metrics:")
print(f"   ├─ R² Score: {train_r2:.4f}")
print(f"   ├─ MSE: ${train_mse:,.2f}")
print(f"   └─ MAE: ${train_mae:,.2f}")

print(f"\n   Testing Metrics:")
print(f"   ├─ R² Score: {test_r2:.4f}")
print(f"   ├─ MSE: ${test_mse:,.2f}")
print(f"   └─ MAE: ${test_mae:,.2f}")

# Feature importance
print(f"\n🔍 Feature Coefficients:")
feature_names = ['sqft', 'bedrooms', 'bathrooms', 'age', 'location']
for name, coef in zip(feature_names, model.coef_):
    print(f"   ├─ {name:12s}: ${coef:>10,.2f}")
print(f"   └─ {'intercept':12s}: ${model.intercept_:>10,.2f}")

# Save model
os.makedirs('models', exist_ok=True)
with open('models/house_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\n💾 Model saved to: models/house_price_model.pkl")
print("="*60)
print("✅ Training Complete! You can now run app.py to start the API server.")
print("="*60 + "\n")