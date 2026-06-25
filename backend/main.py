import os
import joblib
import pandas as pd
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from backend.schemas import YieldInput, FertilizerInput

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Load models at startup — once, not per request
yield_model = joblib.load("models/yield_model.pkl")
fertilizer_model = joblib.load("models/fertilizer_model.pkl")
fertilizer_encoder = joblib.load("models/fertilizer_label_encoder.pkl")

app = FastAPI(
    title="AgriIntel API",
    description="AI-powered agricultural decision support platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "AgriIntel API is running", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/weather")
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 404:
        return {"error": f"City '{city}' not found"}
    if response.status_code == 401:
        return {"error": "Invalid API key"}
    if response.status_code != 200:
        return {"error": f"API error: {response.status_code}"}

    data = response.json()
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity_percent": data["main"]["humidity"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "wind_speed_ms": data["wind"]["speed"],
        "pressure_hpa": data["main"]["pressure"],
    }

@app.post("/predict-fertilizer")
def predict_fertilizer(data: FertilizerInput):
    input_df = pd.DataFrame([{
        "Temparature": data.temperature,
        "Humidity": data.humidity,
        "Moisture": data.moisture,
        "Nitrogen": data.nitrogen,
        "Potassium": data.potassium,
        "Phosphorous": data.phosphorous,
        f"Soil Type_{data.soil_type}": 1,
        f"Crop Type_{data.crop_type}": 1,
    }])

    # Get all columns the model expects and fill missing ones with 0
    model_columns = fertilizer_model.feature_names_in_
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    prediction = fertilizer_model.predict(input_df)[0]
    fertilizer_name = fertilizer_encoder.inverse_transform([prediction])[0]

    return {
        "recommended_fertilizer": fertilizer_name,
        "input_received": data.model_dump()
    }
    
@app.post("/predict-yield")
def predict_yield(data: YieldInput):
    # Build a dict with all numeric features first
    input_dict = {
        "Year": data.year,
        "average_rain_fall_mm_per_year": data.rainfall,
        "pesticides_tonnes": data.pesticides,
        "avg_temp": data.temp,
    }

    # Add one-hot encoded columns for Area and Item
    # The model expects columns like "Area_India", "Item_Wheat" etc.
    input_dict[f"Area_{data.area}"] = 1
    input_dict[f"Item_{data.item}"] = 1

    # Create DataFrame and align to exact columns model was trained on
    input_df = pd.DataFrame([input_dict])
    model_columns = yield_model.feature_names_in_
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    prediction = yield_model.predict(input_df)[0]

    return {
        "predicted_yield_hg_per_ha": round(prediction, 2),
        "predicted_yield_kg_per_ha": round(prediction / 10, 2),
        "input_received": data.model_dump()
    }