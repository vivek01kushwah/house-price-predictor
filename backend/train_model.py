import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# -------------------------------------
# 1. Load Dataset
# -------------------------------------
df = pd.read_csv("data/Bengaluru_House_Data.csv")

# -------------------------------------
# 2. Data Cleaning
# -------------------------------------

# Convert sqft (handle ranges like "1000-1200")
def convert_sqft(x):
    try:
        if "-" in str(x):
            a, b = x.split("-")
            return (float(a) + float(b)) / 2
        return float(x)
    except:
        return None

df["total_sqft"] = df["total_sqft"].apply(convert_sqft)
df = df.dropna(subset=["total_sqft"])

# Extract BHK safely (handle NaN, float, etc.)
def extract_bhk(x):
    try:
        return int(str(x).split()[0])
    except:
        return None

df["bhk"] = df["size"].apply(extract_bhk)
df = df.dropna(subset=["bhk"])
df["bhk"] = df["bhk"].astype(int)

# Keep required columns only
df = df[["location", "total_sqft", "bath", "bhk", "price"]]
df = df.dropna()

# Remove rare locations with <10 samples
location_counts = df["location"].value_counts()
valid_locations = location_counts[location_counts > 10].index
df = df[df["location"].isin(valid_locations)]

# -------------------------------------
# 3. Train Test Split
# -------------------------------------
X = df.drop("price", axis=1)
y = df["price"] * 100000  # Convert lakhs → rupees

# -------------------------------------
# 4. Build ML Pipeline
# -------------------------------------
pipeline = Pipeline(steps=[
    ('encoder', ColumnTransformer(
        transformers=[('location', OneHotEncoder(handle_unknown='ignore'), ['location'])],
        remainder='passthrough'
    )),
    ('model', LinearRegression())
])

# -------------------------------------
# 5. Train Model
# -------------------------------------
pipeline.fit(X, y)

# -------------------------------------
# 6. Save Model
# -------------------------------------
pickle.dump(pipeline, open("model.pkl", "wb"))

print("Model trained and saved as model.pkl successfully!")
