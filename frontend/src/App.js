import React, { useState, useEffect } from 'react';
import { Home, TrendingUp, BarChart3, IndianRupee } from 'lucide-react';

export default function HousePricePrediction() {
  const [formData, setFormData] = useState({
    sqft: '',
    bedrooms: '',
    bathrooms: '',
    location: ''
  });

  const [locations, setLocations] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [showResults, setShowResults] = useState(false);

  // Fetch locations from backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/locations")
      .then(res => res.json())
      .then(data => {
        setLocations(data.locations);
        setFormData(prev => ({ ...prev, location: data.locations[0] }));
      })
      .catch(err => console.log("Error loading locations:", err));
  }, []);

  // Handle inputs
  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Predict Price
  const predictPrice = async () => {
    if (!formData.sqft || !formData.bedrooms || !formData.bathrooms || !formData.location) {
      alert("Please fill all fields.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      setPrediction({
        price: data.price.toFixed(0),
        confidence: data.confidence.toFixed(1),
        r2Score: data.r2Score.toFixed(3),
        mse: data.mse.toFixed(0),
        priceRange: {
          low: data.priceRange.low.toFixed(0),
          high: data.priceRange.high.toFixed(0)
        }
      });

      setShowResults(true);
    } catch (error) {
      console.log("Prediction error:", error);
      alert("Backend error. Check console.");
    }
  };

  const resetForm = () => {
    setFormData({
      sqft: '',
      bedrooms: '',
      bathrooms: '',
      location: locations[0] || ''
    });
    setPrediction(null);
    setShowResults(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 p-6">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Home className="w-10 h-10 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-800">House Price Predictor</h1>
          </div>
          <p className="text-gray-600">AI-Powered Real Estate Valuation Using Kaggle Dataset</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">

          {/* Form Section */}
          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-6">Enter Property Details</h2>

            <div className="space-y-5">

              {/* Sqft */}
              <input
                type="number"
                name="sqft"
                value={formData.sqft}
                onChange={handleInputChange}
                placeholder="Enter total Sqft"
                className="w-full px-4 py-3 border rounded-lg"
              />

              {/* BHK */}
              <input
                type="number"
                name="bedrooms"
                value={formData.bedrooms}
                onChange={handleInputChange}
                placeholder="Enter BHK"
                className="w-full px-4 py-3 border rounded-lg"
              />

              {/* Bathrooms */}
              <input
                type="number"
                name="bathrooms"
                value={formData.bathrooms}
                onChange={handleInputChange}
                placeholder="Enter Number of Bathrooms"
                className="w-full px-4 py-3 border rounded-lg"
              />

              {/* Location Dropdown */}
              <select
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border rounded-lg"
              >
                {locations.map((loc, index) => (
                  <option key={index} value={loc}>{loc}</option>
                ))}
              </select>

              {/* Buttons */}
              <div className="flex gap-4 mt-4">
                <button onClick={predictPrice}
                  className="flex-1 bg-indigo-600 text-white py-3 rounded-lg">
                  Predict Price
                </button>

                <button onClick={resetForm}
                  className="px-6 py-3 border rounded-lg">
                  Reset
                </button>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-6">Prediction Results</h2>

            {!showResults ? (
              <div className="text-gray-400 text-center h-64 flex flex-col items-center justify-center">
                <IndianRupee className="w-16 h-16 mb-4" />
                Enter values to predict the house price
              </div>
            ) : (
              <div className="space-y-6">

                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 rounded-xl text-white">
                  <p className="text-sm opacity-80">Estimated Price</p>
                  <p className="text-4xl font-bold">₹{parseInt(prediction.price).toLocaleString('en-IN')}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    Confidence: <span className="font-bold text-blue-600">{prediction.confidence}%</span>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    R² Score: <span className="font-bold text-green-600">{prediction.r2Score}</span>
                  </div>
                </div>

              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
