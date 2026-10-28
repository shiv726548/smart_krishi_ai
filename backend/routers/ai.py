from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import Literal

from backend.database import get_db
from backend.models import AIDiagnosis, User
from backend.security import get_current_user
from backend.ai_engine.model_pipeline import (
    MAX_IMAGE_BYTES,
    InvalidPlantImage,
    plant_ai_pipeline,
)

router = APIRouter(prefix="/api/ai", tags=["AI Plant Health Scanner"])


@router.post("/scan-plant")
async def scan_plant_health(
    file: UploadFile = File(...),
    crop_type: Literal["Tomato", "Potato", "Rice", "Wheat", "Cotton", "Corn"] = Form("Tomato"),
    language: Literal["en", "hi", "mr"] = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    del db, current_user  # Scans are not stored until a real model is integrated.
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=415,
            detail="Use a JPEG, PNG, or WebP image",
        )
    image_bytes = await file.read(MAX_IMAGE_BYTES + 1)
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image is too large; maximum is 5 MB")
    try:
        diagnosis = plant_ai_pipeline.analyze_image(
            image_bytes=image_bytes,
            crop_hint=crop_type,
            lang=language,
        )
    except InvalidPlantImage as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "unavailable", "diagnosis": diagnosis}


@router.get("/history/{user_id}")
def get_user_ai_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot access another farmer's history")
    records = (
        db.query(AIDiagnosis)
        .filter(AIDiagnosis.user_id == current_user.id)
        .order_by(AIDiagnosis.timestamp.desc())
        .all()
    )
    return {
        "status": "success",
        "count": len(records),
        "warning": (
            "Stored scans from earlier versions used an untrained heuristic. "
            "They are unverified and must not be treated as diagnoses."
        ),
        "history": [
            {
                "id": record.id,
                "crop": record.crop_type,
                "disease": "Unverified legacy output — not a diagnosis",
                "legacy_label": record.disease_detected,
                "confidence": None,
                "health_status": "Unverified",
                "timestamp": record.timestamp.isoformat(),
                "actions": [
                    "This result came from an untrained demo heuristic. Do not use it to choose treatment."
                ],
            }
            for record in records
        ],
    }
