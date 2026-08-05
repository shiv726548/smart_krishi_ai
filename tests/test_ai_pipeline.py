from backend.ai_engine.model_pipeline import plant_ai_pipeline
from PIL import Image
import io

def test_pytorch_model_pipeline():
    # Create dummy image bytes
    img = Image.new("RGB", (300, 300), color=(200, 100, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    result = plant_ai_pipeline.analyze_image(img_bytes, crop_hint="Tomato", lang="en")
    
    assert "disease_detected" in result
    assert "confidence_percentage" in result
    assert "suggested_actions" in result
    assert result["crop"] == "Tomato"
    print("PyTorch CV Pipeline test passed successfully!")

if __name__ == "__main__":
    test_pytorch_model_pipeline()
