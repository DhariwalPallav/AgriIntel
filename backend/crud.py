from sqlalchemy.orm import Session
from backend import models

def save_yield_prediction(db: Session, input_data, predicted_yield_kg: float):
    record = models.YieldPrediction(
        area=input_data.area,
        item=input_data.item,
        year=input_data.year,
        rainfall=input_data.rainfall,
        pesticides=input_data.pesticides,
        temp=input_data.temp,
        predicted_yield_kg=predicted_yield_kg,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def save_fertilizer_prediction(db: Session, input_data, recommended_fertilizer: str):
    record = models.FertilizerPrediction(
        temperature=input_data.temperature,
        humidity=input_data.humidity,
        moisture=input_data.moisture,
        soil_type=input_data.soil_type,
        crop_type=input_data.crop_type,
        nitrogen=input_data.nitrogen,
        potassium=input_data.potassium,
        phosphorous=input_data.phosphorous,
        recommended_fertilizer=recommended_fertilizer,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_yield_predictions(db: Session, limit: int = 10):
    return db.query(models.YieldPrediction).order_by(
        models.YieldPrediction.created_at.desc()
    ).limit(limit).all()

def get_fertilizer_predictions(db: Session, limit: int = 10):
    return db.query(models.FertilizerPrediction).order_by(
        models.FertilizerPrediction.created_at.desc()
    ).limit(limit).all()
    