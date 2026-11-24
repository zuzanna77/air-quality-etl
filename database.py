import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("output/air_quality.db")


def init_db(db_path: Path = DB_PATH) -> None:
    """Tworzy tabelę pomiarów, jeśli jeszcze nie istnieje."""
    db_path.parent.mkdir(exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                time TEXT NOT NULL,
                date TEXT NOT NULL,
                hour INTEGER NOT NULL,
                pm10 REAL,
                pm2_5 REAL,
                nitrogen_dioxide REAL,
                pm10_exceeded INTEGER,
                pm2_5_exceeded INTEGER,
                UNIQUE(city, time)
            )
        """)


def save_to_db(df: pd.DataFrame, city: str, db_path: Path = DB_PATH) -> int:
    """Zapisuje oczyszczone dane do bazy SQLite bez tworzenia duplikatów."""
    records = [
        (
            city,
            str(row["time"]),
            row["date"],
            int(row["hour"]),
            None if pd.isna(row["pm10"]) else float(row["pm10"]),
            None if pd.isna(row["pm2_5"]) else float(row["pm2_5"]),
            None if pd.isna(row["nitrogen_dioxide"]) else float(row["nitrogen_dioxide"]),
            int(row["pm10_exceeded"]),
            int(row["pm2_5_exceeded"]),
        )
        for _, row in df.iterrows()
    ]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.executemany(
            """
            INSERT OR REPLACE INTO measurements (
                city, time, date, hour, pm10, pm2_5,
                nitrogen_dioxide, pm10_exceeded, pm2_5_exceeded
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            records,
        )
        return cursor.rowcount


def get_cities_summary(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Pobiera z bazy podsumowanie wszystkich zapisanych miast za pomocą SQL."""
    query = """
        SELECT
            city,
            COUNT(*) AS total_hours,
            ROUND(AVG(pm10), 2) AS avg_pm10,
            ROUND(MAX(pm10), 2) AS max_pm10,
            SUM(pm10_exceeded) AS hours_exceeded
        FROM measurements
        GROUP BY city
        ORDER BY avg_pm10 DESC
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)