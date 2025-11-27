import requests
import json

# API endpoint
url = "http://localhost:5000/predict"

# Test data
test_data = {
    "sqft": 2000,
    "bedrooms": 3,
    "bathrooms": 2,
    "age": 5,
    "location": "urban"
}

print("\n" + "="*50)
print("🧪 Testing House Price Prediction API")
print("="*50)
print("\n📤 Sending request with data:")
print(json.dumps(test_data, indent=2))

try:
    response = requests.post(url, json=test_data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success! Prediction received:")
        print(f"\n💰 Estimated Price: ${result['price']:,.2f}")
        print(f"📊 Confidence: {result['confidence']:.1f}%")
        print(f"📈 Price Range: ${result['priceRange']['low']:,.2f} - ${result['priceRange']['high']:,.2f}")
        print(f"🎯 R² Score: {result['r2Score']:.3f}")
        print(f"📉 MSE: ${result['mse']:,.2f}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Connection Error: {e}")
    print("\nMake sure the Flask server is running (python app.py)")

print("="*50 + "\n")