import io

import pytest
from PIL import Image

from backend.ai_engine.model_pipeline import (
    InvalidPlantImage,
    plant_ai_pipeline,
    validate_plant_image,
)


def make_jpeg() -> bytes:
    image = Image.new("RGB", (64, 64), color=(30, 160, 80))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_pipeline_does_not_claim_a_diagnosis_without_weights():
    result = plant_ai_pipeline.analyze_image(make_jpeg(), crop_hint="Tomato", lang="en")

    assert result["available"] is False
    assert result["disease_detected"] is None
    assert result["confidence_percentage"] is None
    assert "no trained model weights" in result["message"].lower()


@pytest.mark.parametrize("content", [b"", b"not an image"])
def test_invalid_image_is_rejected(content):
    with pytest.raises(InvalidPlantImage):
        validate_plant_image(content)


def test_oversized_image_is_rejected():
    with pytest.raises(InvalidPlantImage, match="5 MB"):
        validate_plant_image(b"x" * (5 * 1024 * 1024 + 1))


def test_unsupported_image_format_is_rejected():
    image = Image.new("RGB", (8, 8), color=(0, 0, 0))
    buffer = io.BytesIO()
    image.save(buffer, format="BMP")
    with pytest.raises(InvalidPlantImage, match="JPEG, PNG, or WebP"):
        validate_plant_image(buffer.getvalue())
