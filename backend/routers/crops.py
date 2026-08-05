from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Crop

router = APIRouter(prefix="/api/crops", tags=["Crop Management"])

class CropCreate(BaseModel):
    user_id: int = 1
    crop_name: str # Tomato, Potato, Rice, Wheat, Cotton, Corn
    variety: Optional[str] = "Hybrid Super 30"
    sowing_date: str # YYYY-MM-DD
    field_size_acres: float = 2.5
    farm_location: str = "North Field Sector 2"
    growth_stage: Optional[str] = "Vegetative"
    target_moisture_min: Optional[float] = 40.0
    target_moisture_max: Optional[float] = 70.0

@router.post("/add")
def add_crop(crop_data: CropCreate, db: Session = Depends(get_db)):
    new_crop = Crop(
        user_id=crop_data.user_id,
        crop_name=crop_data.crop_name,
        variety=crop_data.variety,
        sowing_date=crop_data.sowing_date,
        field_size_acres=crop_data.field_size_acres,
        farm_location=crop_data.farm_location,
        growth_stage=crop_data.growth_stage,
        target_moisture_min=crop_data.target_moisture_min,
        target_moisture_max=crop_data.target_moisture_max
    )
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    return {
        "status": "success",
        "message": "Crop profile added successfully",
        "crop": {
            "id": new_crop.id,
            "name": new_crop.crop_name,
            "growth_stage": new_crop.growth_stage,
            "sowing_date": new_crop.sowing_date
        }
    }

@router.get("/user/{user_id}")
def list_farmer_crops(user_id: int, db: Session = Depends(get_db)):
    crops = db.query(Crop).filter(Crop.user_id == user_id, Crop.is_active == True).all()
    
    # Generate schedule & tips dynamically
    result_list = []
    for c in crops:
        schedule = [
            {"day": "Day 1-15", "task": "Germination & Rooting", "status": "Completed"},
            {"day": "Day 16-45", "task": "Vegetative Growth & Nitrogen Top Dressing", "status": "In Progress"},
            {"day": "Day 46-75", "task": "Flowering & Micro-nutrient Spray", "status": "Upcoming"},
            {"day": "Day 76-110", "task": "Fruit Development & Harvest Prep", "status": "Upcoming"}
        ]
        tips = [
            "Maintain soil moisture between 40-70% for optimal growth.",
            "Scout for sucking pests under lower leaf surfaces every 3 days.",
            "Apply bio-fungicide during cloudy weather to prevent blights."
        ]
        result_list.append({
            "id": c.id,
            "crop_name": c.crop_name,
            "variety": c.variety,
            "sowing_date": c.sowing_date,
            "field_size_acres": c.field_size_acres,
            "farm_location": c.farm_location,
            "growth_stage": c.growth_stage,
            "target_moisture_min": c.target_moisture_min,
            "target_moisture_max": c.target_moisture_max,
            "schedule": schedule,
            "tips": tips
        })

    return {
        "status": "success",
        "count": len(result_list),
        "crops": result_list
    }
