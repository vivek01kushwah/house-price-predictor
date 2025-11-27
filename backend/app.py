from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle

# ---------------------------------------
# Create Flask App + Enable CORS
# ---------------------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------------------
# Load ML Model
# ---------------------------------------
model = pickle.load(open("model.pkl", "rb"))

# Load CSV to get locations
df = pd.read_csv("data/Bengaluru_House_Data.csv")


# ---------------------------------------
# API: Get all locations (for dropdown)
# ---------------------------------------
@app.route("/locations", methods=["GET"])
def get_locations():
    location_counts = df["location"].value_counts()
    valid_locations = list(location_counts[location_counts > 10].index)
    return jsonify({"locations": valid_locations})


# ---------------------------------------
# Root Route
# ---------------------------------------
@app.route("/", methods=["GET"])
def home():
    return "House Price Prediction API is running!"


# ---------------------------------------
# Prediction Route
# ---------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Extract required fields from React
        sqft = float(data["sqft"])
        bhk = int(data["bedrooms"])    # same as BHK
        bath = int(data["bathrooms"])
        location = data["location"]

        # Prepare input for model
        input_data = pd.DataFrame(
            [[location, sqft, bath, bhk]],
            columns=["location", "total_sqft", "bath", "bhk"]
        )

        # Predict using trained model
        predicted_price = model.predict(input_data)[0]   # already in INR

        # Confidence & Range (dummy values)
        price_range = {
            "low": float(predicted_price * 0.9),
            "high": float(predicted_price * 1.1)
        }

        return jsonify({
            "price": float(predicted_price),
            "confidence": 87.5,
            "priceRange": price_range,
            "r2Score": 0.875,
            "mse": 45000,
            "currency": "INR"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---------------------------------------
# Run Flask Server
# ---------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
