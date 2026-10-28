from typing import Literal
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Crop, User
from backend.security import get_current_user

router = APIRouter(prefix="/api/crops", tags=["Crop Management"])


class CropCreate(BaseModel):
    crop_name: Literal["Tomato", "Potato", "Rice", "Wheat", "Cotton", "Corn"]
    variety: str = Field(default="Standard", max_length=100)
    sowing_date: date
    field_size_acres: float = Field(default=1.0, gt=0, le=100000)
    farm_location: str = Field(default="Field A", max_length=160)
    growth_stage: str = Field(default="Vegetative", max_length=40)
    target_moisture_min: float = Field(default=40.0, ge=0, le=100)
    target_moisture_max: float = Field(default=70.0, ge=0, le=100)


@router.post("/add")
def add_crop(
    crop_data: CropCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if crop_data.target_moisture_min >= crop_data.target_moisture_max:
        raise HTTPException(
            status_code=422,
            detail="Minimum moisture target must be lower than the maximum",
        )
    new_crop = Crop(
        user_id=current_user.id,
        crop_name=crop_data.crop_name,
        variety=crop_data.variety,
        sowing_date=crop_data.sowing_date.isoformat(),
        field_size_acres=crop_data.field_size_acres,
        farm_location=crop_data.farm_location,
        growth_stage=crop_data.growth_stage,
        target_moisture_min=crop_data.target_moisture_min,
        target_moisture_max=crop_data.target_moisture_max,
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
            "sowing_date": new_crop.sowing_date,
        },
    }


@router.get("/user/{user_id}")
def list_farmer_crops(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot access another farmer's crops")
    crops = (
        db.query(Crop)
        .filter(Crop.user_id == current_user.id, Crop.is_active.is_(True))
        .all()
    )
    result_list = []
    for crop in crops:
        try:
            days_since_sowing = max(
                (date.today() - date.fromisoformat(crop.sowing_date)).days, 0
            )
        except (TypeError, ValueError):
            days_since_sowing = None

        def window_status(start_day: int, end_day: int) -> str:
            if days_since_sowing is None:
                return "Unknown — check sowing date"
            if start_day <= days_since_sowing <= end_day:
                return "Current window"
            if days_since_sowing < start_day:
                return "Upcoming"
            return "Past window"

        schedule = [
            {
                "day": "Day 1-15",
                "task": "Root establishment check",
                "status": window_status(1, 15),
            },
            {
                "day": "Day 16-45",
                "task": "Vegetative growth check",
                "status": window_status(16, 45),
            },
            {
                "day": "Day 46-75",
                "task": "Flowering and crop-health check",
                "status": window_status(46, 75),
            },
            {
                "day": "Day 76-110",
                "task": "Harvest-readiness check",
                "status": window_status(76, 110),
            },
        ]
        tips = [
            "Use the configured moisture range for this crop.",
            "Inspect plants regularly for pests and disease symptoms.",
            "Confirm local advice before applying any pesticide or fertilizer.",
        ]
        result_list.append(
            {
                "id": crop.id,
                "crop_name": crop.crop_name,
                "variety": crop.variety,
                "sowing_date": crop.sowing_date,
                "field_size_acres": crop.field_size_acres,
                "farm_location": crop.farm_location,
                "growth_stage": crop.growth_stage,
                "target_moisture_min": crop.target_moisture_min,
                "target_moisture_max": crop.target_moisture_max,
                "schedule": schedule,
                "tips": tips,
            }
        )
    return {"status": "success", "count": len(result_list), "crops": result_list}
