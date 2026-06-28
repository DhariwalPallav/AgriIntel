import os
import joblib
import pandas as pd
import requests
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from backend.schemas import YieldInput, FertilizerInput
from backend.database import engine, get_db, Base
from backend import models, crud

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Create all tables in the database on startup
Base.metadata.create_all(bind=engine)

# Load ML models once at startup
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
def predict_fertilizer(data: FertilizerInput, db: Session = Depends(get_db)):
    input_dict = {
        "Temparature": data.temperature,
        "Humidity": data.humidity,
        "Moisture": data.moisture,
        "Nitrogen": data.nitrogen,
        "Potassium": data.potassium,
        "Phosphorous": data.phosphorous,
        f"Soil Type_{data.soil_type}": 1,
        f"Crop Type_{data.crop_type}": 1,
    }
    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(
        columns=fertilizer_model.feature_names_in_, fill_value=0
    )
    prediction = fertilizer_model.predict(input_df)[0]
    fertilizer_name = fertilizer_encoder.inverse_transform([prediction])[0]

    # Save to database
    record = crud.save_fertilizer_prediction(db, data, fertilizer_name)

    return {
        "recommended_fertilizer": fertilizer_name,
        "prediction_id": record.id,
        "input_received": data.model_dump()
    }

@app.post("/predict-yield")
def predict_yield(data: YieldInput, db: Session = Depends(get_db)):
    input_dict = {
        "Year": data.year,
        "average_rain_fall_mm_per_year": data.rainfall,
        "pesticides_tonnes": data.pesticides,
        "avg_temp": data.temp,
        f"Area_{data.area}": 1,
        f"Item_{data.item}": 1,
    }
    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(
        columns=yield_model.feature_names_in_, fill_value=0
    )
    prediction = float(yield_model.predict(input_df)[0])
    predicted_kg = float(round(prediction / 10, 2))

    # Save to database
    print(type(prediction))
    print(type(predicted_kg))
    print(predicted_kg)
    record = crud.save_yield_prediction(db, data, predicted_kg)

    return {
        "predicted_yield_hg_per_ha": round(prediction, 2),
        "predicted_yield_kg_per_ha": predicted_kg,
        "prediction_id": record.id,
        "input_received": data.model_dump()
    }

@app.get("/predictions/yield")
def get_yield_history(limit: int = 10, db: Session = Depends(get_db)):
    records = crud.get_yield_predictions(db, limit=limit)
    return {"predictions": [
        {
            "id": r.id,
            "area": r.area,
            "item": r.item,
            "year": r.year,
            "predicted_yield_kg": r.predicted_yield_kg,
            "created_at": str(r.created_at)
        } for r in records
    ]}

@app.get("/predictions/fertilizer")
def get_fertilizer_history(limit: int = 10, db: Session = Depends(get_db)):
    records = crud.get_fertilizer_predictions(db, limit=limit)
    return {"predictions": [
        {
            "id": r.id,
            "crop_type": r.crop_type,
            "soil_type": r.soil_type,
            "recommended_fertilizer": r.recommended_fertilizer,
            "created_at": str(r.created_at)
        } for r in records
    ]}