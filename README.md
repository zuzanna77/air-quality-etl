# Air Quality ETL & Data Quality Analyzer

Aplikacja w języku Python realizująca kompletny potok **ETL (Extract → Transform → Load)** dla danych o jakości powietrza. Narzędzie pobiera historyczne pomiary stężeń pyłów zawieszonych (PM10, PM2.5) oraz dwutlenku azotu (NO₂) dla wybranych polskich miast z publicznego API **Open-Meteo Air Quality**, weryfikuje ich jakość, czyści dane oraz generuje raporty analityczne.

## Główne funkcjonalności

* **Extract (Pobieranie):** Komunikacja z REST API za pomocą parametryzowanych zapytań HTTP (`requests`) z obsługą błędów sieciowych i statusów odpowiedzi.
* **Transform (Walidacja i analiza):**
  * Konwersja surowych danych JSON do struktury `pandas.DataFrame`.
  * Ocena jakości danych: zliczanie brakujących wartości (`NaN`) oraz wykrywanie anomalii czujników (wartości ujemne).
  * Czyszczenie zbioru oraz flagowanie godzin z przekroczeniem dobowych norm jakości powietrza (PM10 > 50 µg/m³, PM2.5 > 25 µg/m³).
  * Obliczanie dziennych statystyk (`groupby`, `agg`): średnia, mediana, maksimum oraz liczba godzin z przekroczeniem normy.
* **Load (Eksport):** Zapis oczyszczonych danych i statystyk dziennych do plików `.csv` oraz raportu jakościowego do pliku `.json`.

## Technologie

* Python 3.x
* `requests`
* `pandas`

## Struktura projektu

```text
air-quality-etl/
├── main.py              # Główny skrypt uruchamiający aplikację
├── api_client.py        # Moduł odpowiedzialny za pobieranie danych z API
├── processor.py         # Walidacja, czyszczenie i agregacja danych (pandas)
├── config.py            # Konfiguracja miast (współrzędne) oraz norm jakości powietrza
├── requirements.txt     # Lista wymaganych bibliotek
├── output/              # Wygenerowane pliki wynikowe (CSV oraz JSON)
└── README.md            # Dokumentacja projektu