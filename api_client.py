import requests
from config import API_URL


def fetch_air_quality(latitude: float, longitude: float, past_days: int = 7) -> dict:
    """Pobiera godzinowe dane o jakości powietrza z Open-Meteo API."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm10,pm2_5,nitrogen_dioxide",
        "past_days": past_days,
        "timezone": "Europe/Warsaw",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Błąd podczas pobierania danych z API: {e}")