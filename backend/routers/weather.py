from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/weather", tags=["Weather Forecast"])


@router.get("/current")
def get_weather_forecast(
    location: str = Query(default="Maharashtra, India", min_length=2, max_length=120)
):
    """Return an honest unavailable state rather than fabricated live conditions."""
    return {
        "status": "unavailable",
        "data_source": "unavailable",
        "location": location,
        "current": None,
        "forecast": [],
        "irrigation_recommendation": {
            "action": "UNAVAILABLE",
            "advice": (
                "Live weather is not configured. Use verified local weather "
                "information and soil readings before changing irrigation."
            ),
        },
    }
