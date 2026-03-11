# House Price Predictor (Bangalore)

A full-stack Machine Learning project that predicts **Bangalore house prices** based on inputs like **location, total_sqft, BHK, bathrooms**.  
It includes:

- **Backend (Flask API)**: serves prediction + locations list
- **Frontend (React)**: UI to enter property details and view predicted price
- Model trained on **Kaggle Bangalore House Price dataset** (preprocessing + Linear Regression pipeline)

---

## Project Structure

```text
house-price-predictor/
├─ backend/
│  ├─ app.py
│  ├─ train_model.py
│  ├─ model.pkl
│  ├─ requirements.txt
│  ├─ data/
│  └─ models/
└─ frontend/
   ├─ package.json
   ├─ .env
   └─ src/
```

---

## Features

- Dropdown of **valid locations** fetched from backend (`/locations`)
- Predicts price via backend (`/predict`)
- Uses an ML pipeline with:
  - **OneHotEncoder** for `location`
  - **LinearRegression** model
- Displays result in **INR (₹)** in the UI

---

## Tech Stack

**Backend**
- Python, Flask, Flask-CORS
- pandas, numpy, scikit-learn
- gunicorn (for deployment)

**Frontend**
- React (Create React App)
- TailwindCSS
- lucide-react icons

---

## Backend API

Base URL (local): `http://127.0.0.1:5000`

### `GET /`
Health check.

**Response**
- `House Price Prediction API is running!`

### `GET /locations`
Returns filtered locations (only those with enough samples).

**Response example**
```json
{
  "locations": ["Whitefield", "Electronic City", "..."]
}
```

### `POST /predict`
Predicts house price.

**Request JSON**
```json
{
  "sqft": 1200,
  "bedrooms": 2,
  "bathrooms": 2,
  "location": "Whitefield"
}
```

**Response JSON (example)**
```json
{
  "price": 9500000,
  "confidence": 87.5,
  "priceRange": { "low": 8550000, "high": 10450000 },
  "r2Score": 0.875,
  "mse": 45000,
  "currency": "INR"
}
```

---

## Setup & Run Locally

### 1) Clone the repo
```bash
git clone https://github.com/vivek01kushwah/house-price-predictor.git
cd house-price-predictor
```

---

## Backend Setup (Flask)

### 2) Create venv + install dependencies
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3) Train model (creates `model.pkl`)
Make sure dataset exists at:
```text
backend/data/Bengaluru_House_Data.csv
```

Then run:
```bash
python train_model.py
```

### 4) Start backend server
```bash
python app.py
```

Backend will run (debug) at:
- `http://127.0.0.1:5000`

---

## Frontend Setup (React)

### 5) Install dependencies
```bash
cd ../frontend
npm install
```

### 6) Configure API URL
Edit `frontend/.env` to point to your backend, for example:
```env
REACT_APP_API_URL=http://127.0.0.1:5000
```

### 7) Start frontend
```bash
npm start
```

Frontend runs at:
- `http://localhost:3000`

---

## Notes / Common Issues

- If frontend shows empty locations:
  - Ensure backend is running
  - Ensure `REACT_APP_API_URL` is correct in `frontend/.env`
- If backend errors loading dataset:
  - Verify file exists: `backend/data/Bengaluru_House_Data.csv`
- If prediction fails:
  - Check backend logs and confirm `model.pkl` exists in `backend/`

---

## Future Improvements

- Add input validation + better error messages
- Add model metrics page (R², MAE, etc.)
- Add Docker support for one-command run
- Deploy (Render/Heroku for backend + Netlify/Vercel for frontend)

---

## License

This project is for learning and demonstration purposes.