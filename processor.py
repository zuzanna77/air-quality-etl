import pandas as pd
from config import NORMS


def build_dataframe(raw_data: dict) -> pd.DataFrame:
    """Zamienia sekcję 'hourly' z JSON-a na pandas DataFrame."""
    hourly = raw_data.get("hourly", {})
    df = pd.DataFrame(hourly)

    # Konwersja czasu na typ datetime i rozdzielenie na datę oraz godzinę
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date.astype(str)
    df["hour"] = df["time"].dt.hour

    return df


def analyze_quality(df: pd.DataFrame) -> dict:
    """Sprawdza braki danych oraz ewentualne anomalie (wartości ujemne)."""
    total_rows = len(df)
    missing_values = df[["pm10", "pm2_5", "nitrogen_dioxide"]].isna().sum().to_dict()

    negative_values = {
        col: int((df[col] < 0).sum())
        for col in ["pm10", "pm2_5", "nitrogen_dioxide"]
    }

    return {
        "total_records": total_rows,
        "missing_values": missing_values,
        "negative_anomalies": negative_values,
    }


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Usuwa niepoprawne rekordy i dodaje kolumny z przekroczeniami norm."""
    cleaned = df.copy()

    # Zamiana wartości ujemnych (błędy czujników) na NaN
    for col in ["pm10", "pm2_5", "nitrogen_dioxide"]:
        cleaned.loc[cleaned[col] < 0, col] = pd.NA

    # Usunięcie wierszy, gdzie brakuje jednocześnie PM10 i PM2.5
    cleaned = cleaned.dropna(subset=["pm10", "pm2_5"], how="all")

    # Flagi przekroczeń norm
    cleaned["pm10_exceeded"] = cleaned["pm10"] > NORMS["pm10"]
    cleaned["pm2_5_exceeded"] = cleaned["pm2_5"] > NORMS["pm2_5"]

    return cleaned


def compute_daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Grupuje dane po dacie i oblicza statystyki dzienne."""
    daily = (
        df.groupby("date")
        .agg(
            pm10_mean=("pm10", "mean"),
            pm10_median=("pm10", "median"),
            pm10_max=("pm10", "max"),
            pm2_5_mean=("pm2_5", "mean"),
            pm10_hours_exceeded=("pm10_exceeded", "sum"),
        )
        .round(2)
        .reset_index()
    )
    return daily