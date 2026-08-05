from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    location = Column(String, default="Maharashtra, India")
    preferred_language = Column(String, default="en") # en, hi, mr
    created_at = Column(DateTime, default=datetime.utcnow)

    crops = relationship("Crop", back_populates="owner")
    telemetry_logs = relationship("SensorData", back_populates="user")
    ai_diagnoses = relationship("AIDiagnosis", back_populates="user")

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    crop_name = Column(String, nullable=False) # Tomato, Potato, Rice, Wheat, Cotton, Corn
    variety = Column(String, default="Standard Hybrid")
    sowing_date = Column(String, nullable=False)
    field_size_acres = Column(Float, default=1.0)
    farm_location = Column(String, default="Field A")
    growth_stage = Column(String, default="Vegetative") # Seedling, Vegetative, Flowering, Fruiting, Harvest
    target_moisture_min = Column(Float, default=40.0) # %
    target_moisture_max = Column(Float, default=70.0) # %
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="crops")

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    device_id = Column(String, default="ESP32_KRISHI_01")
    soil_moisture = Column(Float, nullable=False) # percentage 0 - 100%
    temperature = Column(Float, nullable=False) # Celsius
    humidity = Column(Float, nullable=False) # percentage
    nitrogen = Column(Float, default=45.0) # mg/kg optional sensor
    phosphorus = Column(Float, default=25.0) # mg/kg
    potassium = Column(Float, default=60.0) # mg/kg
    pump_status = Column(Boolean, default=False)
    battery_level = Column(Float, default=95.0) # percentage
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="telemetry_logs")

class AIDiagnosis(Base):
    __tablename__ = "ai_diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    crop_type = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    disease_detected = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    health_status = Column(String, nullable=False) # Healthy, Diseased, Nutrient Deficient
    suggested_actions = Column(Text, nullable=False)
    chemical_treatment = Column(Text, nullable=True)
    organic_treatment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ai_diagnoses")

class IrrigationLog(Base):
    __tablename__ = "irrigation_logs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, default="ESP32_KRISHI_01")
    trigger_type = Column(String, nullable=False) # AUTO_MOISTURE_LOW, MANUAL_APP, TIMER
    action = Column(String, nullable=False) # TURN_ON, TURN_OFF, SAFETY_TIMEOUT
    soil_moisture_at_trigger = Column(Float, nullable=False)
    duration_seconds = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
