from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class YieldPrediction(Base):
    __tablename__ = "yield_predictions"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(String)
    item = Column(String)
    year = Column(Integer)
    rainfall = Column(Float)
    pesticides = Column(Float)
    temp = Column(Float)
    predicted_yield_kg = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FertilizerPrediction(Base):
    __tablename__ = "fertilizer_predictions"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    moisture = Column(Float)
    soil_type = Column(String)
    crop_type = Column(String)
    nitrogen = Column(Integer)
    potassium = Column(Integer)
    phosphorous = Column(Integer)
    recommended_fertilizer = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())