from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import AIDiagnosis
from backend.ai_engine.model_pipeline import plant_ai_pipeline
import base64

router = APIRouter(prefix="/api/ai", tags=["AI Plant Health Scanner"])

@router.post("/scan-plant")
async def scan_plant_health(
    file: UploadFile = File(...),
    crop_type: str = Form("Tomato"),
    user_id: int = Form(1),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    """
    Accepts plant/leaf camera image upload, runs PyTorch Computer Vision AI model,
    returns disease detection result, confidence score, and multi-lingual remedies.
    """
    try:
        image_bytes = await file.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded image file is empty")

        # Execute Computer Vision Pipeline
        result = plant_ai_pipeline.analyze_image(
            image_bytes=image_bytes,
            crop_hint=crop_type,
            lang=language
        )

        # Store diagnosis history in DB
        db_diagnosis = AIDiagnosis(
            user_id=user_id,
            crop_type=crop_type,
            disease_detected=result["disease_detected"],
            confidence=result["confidence_percentage"],
            health_status=result["health_status"],
            suggested_actions="\n".join(result["suggested_actions"]),
            chemical_treatment=result["chemical_treatment"],
            organic_treatment=result["organic_treatment"]
        )
        db.add(db_diagnosis)
        db.commit()

        return {
            "status": "success",
            "diagnosis": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Plant Scan Error: {str(e)}")

@router.get("/history/{user_id}")
def get_user_ai_history(user_id: int, db: Session = Depends(get_db)):
    """
    Returns historical plant disease scans for the farmer.
    """
    records = db.query(AIDiagnosis).filter(AIDiagnosis.user_id == user_id).order_by(AIDiagnosis.timestamp.desc()).all()
    return {
        "status": "success",
        "count": len(records),
        "history": [
            {
                "id": r.id,
                "crop": r.crop_type,
                "disease": r.disease_detected,
                "confidence": r.confidence,
                "health_status": r.health_status,
                "timestamp": r.timestamp.isoformat(),
                "actions": r.suggested_actions.split("\n")
            }
            for r in records
        ]
    }
