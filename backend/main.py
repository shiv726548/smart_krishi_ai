from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import engine, Base
from backend.routers import auth, sensors, ai, assistant, crops, weather

import os


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Smart Krishi AI - Backend API",
    description=(
        "IoT & AI Agriculture Assistant Backend for Crop Monitoring, "
        "Plant Health, and Automated Irrigation"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(ai.router)
app.include_router(assistant.router)
app.include_router(crops.router)
app.include_router(weather.router)


# ============================================================
# WEB APP PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WEB_APP_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../web_app")
)


# ============================================================
# SERVE FRONTEND
# ============================================================

if os.path.exists(WEB_APP_PATH):

    # Main application
    @app.get("/app")
    async def web_app():
        return FileResponse(
            os.path.join(WEB_APP_PATH, "index.html")
        )

    # JavaScript
    @app.get("/app.js")
    async def app_js():
        return FileResponse(
            os.path.join(WEB_APP_PATH, "app.js"),
            media_type="application/javascript"
        )

    # CSS
    @app.get("/style.css")
    async def style_css():
        return FileResponse(
            os.path.join(WEB_APP_PATH, "style.css"),
            media_type="text/css"
        )

    # Static assets
    app.mount(
        "/static",
        StaticFiles(directory=WEB_APP_PATH),
        name="static"
    )


# ============================================================
# ROOT API
# ============================================================

@app.get("/")
def root():
    return {
        "app": "Smart Krishi AI System API",
        "status": "Online & Operational",
        "documentation": "/docs",
        "web_dashboard": "/app"
    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )