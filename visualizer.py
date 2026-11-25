import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = Path("output/air_quality.db")
OUTPUT_DIR = Path("output")


def plot_daily_air_quality(db_path: Path = DB_PATH) -> None:
    if not db_path.exists():
        print(f"Nie znaleziono bazy danych: {db_path}")
        return

    with sqlite3.connect(db_path) as conn:
        query = """
            SELECT
                city,
                date,
                ROUND(AVG(pm10), 2) AS avg_pm10,
                ROUND(AVG(pm2_5), 2) AS avg_pm2_5
            FROM measurements
            GROUP BY city, date
            ORDER BY date;
        """
        df = pd.read_sql_query(query, conn)

    if df.empty:
        print("Brak danych do narysowania wykresu.")
        return

    for city, city_df in df.groupby("city"):
        plt.figure(figsize=(10, 5))
        plt.plot(city_df["date"], city_df["avg_pm10"], marker="o", label="PM10 (µg/m³)")
        plt.plot(city_df["date"], city_df["avg_pm2_5"], marker="s", label="PM2.5 (µg/m³)")

        # Linia normy dobowej PM10 (50 µg/m³)
        plt.axhline(y=50, color="red", linestyle="--", linewidth=1, label="Norma PM10 (50 µg/m³)")

        plt.title(f"Średnie dobowe stężenie PM10 i PM2.5 – {city}")
        plt.xlabel("Data")
        plt.ylabel("Stężenie (µg/m³)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend()
        plt.tight_layout()

        output_file = OUTPUT_DIR / f"{city.lower()}_air_quality.png"
        plt.savefig(output_file, dpi=150)
        plt.close()
        print(f"Zapisano wykres: {output_file}")


if __name__ == "__main__":
    plot_daily_air_quality()