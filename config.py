API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

CITIES = {
    "Krakow": {"latitude": 50.0647, "longitude": 19.9450},
    "Warszawa": {"latitude": 52.2297, "longitude": 21.0122},
    "Gdansk": {"latitude": 54.3520, "longitude": 18.6466},
    "Wroclaw": {"latitude": 51.1079, "longitude": 17.0385},
    "Zakopane": {"latitude": 49.2992, "longitude": 19.9496},
}

# Dobowe normy jakości powietrza (µg/m³)
NORMS = {
    "pm10": 50.0,
    "pm2_5": 25.0,
}
# Progi dobowe (µg/m³) - PM10: 50, PM2.5: 25.
# WHO (wytyczne 2021) zaleca niższe wartości: 45 / 15.
NORMS = {
    "pm10": 50.0,
    "pm2_5": 25.0,
}