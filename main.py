import json
from pathlib import Path
from config import CITIES
from api_client import fetch_air_quality
from processor import (
    build_dataframe,
    analyze_quality,
    clean_and_enrich,
    compute_daily_stats,
)


def main():
    print("Dostępne miasta:", ", ".join(CITIES.keys()))
    city = input("Wybierz miasto: ").strip()

    if city not in CITIES:
        print(f"Nieznane miasto: {city}. Wybierz jedno z listy.")
        return

    days_input = input("Ile dni wstecz pobrać? (1-14, domyślnie 7): ").strip()
    past_days = int(days_input) if days_input.isdigit() and 1 <= int(days_input) <= 14 else 7

    coords = CITIES[city]
    print(f"\nPobieranie danych dla: {city} ({past_days} dni)...")

    raw_data = fetch_air_quality(coords["latitude"], coords["longitude"], past_days)
    df = build_dataframe(raw_data)

    quality_report = analyze_quality(df)
    cleaned_df = clean_and_enrich(df)
    daily_stats = compute_daily_stats(cleaned_df)

    # Zapis wyników do folderu output/
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    csv_path = output_dir / f"{city.lower()}_cleaned.csv"
    stats_path = output_dir / f"{city.lower()}_daily_stats.csv"
    report_path = output_dir / f"{city.lower()}_quality_report.json"

    cleaned_df.to_csv(csv_path, index=False)
    daily_stats.to_csv(stats_path, index=False)

    full_report = {
        "city": city,
        "past_days": past_days,
        "data_quality": quality_report,
        "worst_pm10_day": daily_stats.loc[daily_stats["pm10_max"].idxmax(), "date"],
        "max_pm10_recorded": float(daily_stats["pm10_max"].max()),
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)

    print("\n--- Podsumowanie ---")
    print(daily_stats.to_string(index=False))
    print(f"\nZapisano pliki w folderze '{output_dir}/'.")


if __name__ == "__main__":
    main()