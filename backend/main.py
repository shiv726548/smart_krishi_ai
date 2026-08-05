from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
from backend.routers import auth, sensors, ai, assistant, crops, weather
import os

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Krishi AI - Backend API",
    description="IoT & AI Agriculture Assistant Backend for Crop Monitoring, Plant Health, and Automated Irrigation",
    version="1.0.0"
)

# Enable CORS for Mobile App and Web Interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(ai.router)
app.include_router(assistant.router)
app.include_router(crops.router)
app.include_router(weather.router)

# Mount Web App Static Files if directory exists
web_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web_app"))
if os.path.exists(web_app_path):
    app.mount("/app", StaticFiles(directory=web_app_path, html=True), name="web_app")

@app.get("/")
def root():
    return {
        "app": "Smart Krishi AI System API",
        "status": "Online & Operational",
        "documentation": "/docs",
        "web_dashboard": "/app"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
