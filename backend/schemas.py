from pydantic import BaseModel

class YieldInput(BaseModel):
    area: str        # country name e.g. "India"
    item: str        # crop name e.g. "Wheat"
    year: int        # e.g. 2024
    rainfall: float  # average rainfall mm/year
    pesticides: float # pesticides in tonnes
    temp: float      # average temperature celsius

class FertilizerInput(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str   # Sandy, Loamy, Black, Red, Clayey
    crop_type: str   # Maize, Sugarcane, Cotton, Tobacco, Paddy, etc.
    nitrogen: int
    potassium: int
    phosphorous: int