"""Safe plant-image validation until trained model weights are provided."""

from __future__ import annotations

import io

from PIL import Image, UnidentifiedImageError

MAX_IMAGE_BYTES = 5 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
SUPPORTED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


class InvalidPlantImage(ValueError):
    """Raised when an uploaded image is empty, too large, or not a safe image."""


def validate_plant_image(image_bytes: bytes) -> None:
    if not image_bytes:
        raise InvalidPlantImage("The uploaded image is empty")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise InvalidPlantImage("Image is too large; the maximum size is 5 MB")
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            if image.format not in SUPPORTED_IMAGE_FORMATS:
                raise InvalidPlantImage("Use a JPEG, PNG, or WebP image")
            if image.width <= 0 or image.height <= 0:
                raise InvalidPlantImage("The uploaded image is invalid")
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise InvalidPlantImage("Image dimensions are too large")
            image.verify()
    except InvalidPlantImage:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise InvalidPlantImage("The uploaded file is not a valid supported image")


class AIPlantAnalysisPipeline:
    """Do not claim a diagnosis unless actual trained weights are installed."""

    model_available = False

    def analyze_image(
        self, image_bytes: bytes, crop_hint: str = "Tomato", lang: str = "en"
    ) -> dict:
        validate_plant_image(image_bytes)
        return {
            "available": False,
            "crop": crop_hint,
            "disease_detected": None,
            "health_status": "Unavailable",
            "confidence_percentage": None,
            "cause": None,
            "symptoms": None,
            "suggested_actions": [],
            "chemical_treatment": None,
            "organic_treatment": None,
            "message": (
                "Plant diagnosis is unavailable: no trained model weights are "
                "installed. This image was not classified."
            ),
        }


plant_ai_pipeline = AIPlantAnalysisPipeline()
