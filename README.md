# Air Quality ETL & Data Quality Analyzer

Modułowy pipeline ETL w języku Python, który pobiera historyczne dane o jakości powietrza (PM10, PM2.5) z publicznego REST API, waliduje i czyści zbiór danych, zapisuje zdeduplikowane rekordy w bazie SQLite oraz generuje dzienne statystyki, analityczne raporty SQL i wykresy w Matplotlib.

## Przykładowa wizualizacja

![Średnie dobowe stężenie PM10 i PM2.5 – Warszawa](output/warszawa_air_quality.png)

## Główne funkcjonalności

- **Extract (Pobieranie):** Pobieranie godzinowych pomiarów jakości powietrza z publicznego REST API (`requests`) z obsługą parametrów zapytań i błędów.
- **Transform & Validate (Przetwarzanie i walidacja):** Wykorzystanie biblioteki `pandas` do wykrywania brakujących wartości i anomalii sensorów, czyszczenia surowych pomiarów, oznaczania przekroczeń norm oraz obliczania dziennych agregacji.
- **Load & Persist (Zapis danych):** Zapisywanie zdeduplikowanych rekordów w lokalnej bazie SQLite (`database.py`) oraz eksport oczyszczonych danych, statystyk dobowych i raportów jakości danych do plików CSV i JSON.
- **Analityka SQL:** Zestaw zapytań analitycznych (`queries.sql`) wykorzystujących `GROUP BY`, `CASE WHEN`, `HAVING`, CTE (`WITH`) oraz funkcje okna (`ROW_NUMBER()`).
- **Wizualizacja:** Generowanie wykresów dziennych trendów PM10 i PM2.5 wraz z linią normy dobowej za pomocą `Matplotlib` (`visualizer.py`).

## Technologie

- **Język:** Python 3
- **Przetwarzanie i wizualizacja danych:** `pandas`, `matplotlib`
- **API i przechowywanie danych:** `requests`, `sqlite3`, JSON, CSV
- **Analityka:** SQL (SQLite)

## Struktura projektu

```text
air-quality-etl/
├── main.py             # Główny plik uruchamiający cały pipeline ETL
├── processor.py        # Walidacja, czyszczenie danych i agregacje dobowe (pandas)
├── database.py         # Inicjalizacja schematu SQLite, zapis bez duplikatów i zapytania podsumowujące
├── visualizer.py       # Skrypt Matplotlib generujący wykresy jakości powietrza
├── queries.sql         # Analityczne zapytania SQL (CASE WHEN, HAVING, CTE, funkcje okna)
├── requirements.txt    # Lista zależności projektu
└── output/             # Wygenerowane raporty CSV/JSON oraz wykresy PNG