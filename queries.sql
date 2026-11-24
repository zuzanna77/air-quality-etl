-- 1. Porównanie ogólnej jakości powietrza między miastami
SELECT
    city,
    COUNT(*) AS total_hours,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(pm2_5), 2) AS avg_pm2_5,
    ROUND(MAX(pm10), 2) AS max_pm10,
    SUM(pm10_exceeded) AS pm10_hours_exceeded
FROM measurements
GROUP BY city
ORDER BY avg_pm10 DESC;


-- 2. Średnie stężenie PM10 w podziale na pory dnia (CASE WHEN)
SELECT
    city,
    CASE
        WHEN hour BETWEEN 6 AND 11 THEN '1. Rano (06-11)'
        WHEN hour BETWEEN 12 AND 17 THEN '2. Popołudnie (12-17)'
        WHEN hour BETWEEN 18 AND 23 THEN '3. Wieczór (18-23)'
        ELSE '4. Noc (00-05)'
    END AS time_of_day,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(pm2_5), 2) AS avg_pm2_5
FROM measurements
GROUP BY city, time_of_day
ORDER BY city, time_of_day;


-- 3. Dni, w których średnie dobowe stężenie PM10 przekroczyło 30 µg/m³ (HAVING)
SELECT
    city,
    date,
    ROUND(AVG(pm10), 2) AS daily_avg_pm10,
    SUM(pm10_exceeded) AS hours_above_norm
FROM measurements
GROUP BY city, date
HAVING AVG(pm10) > 30
ORDER BY daily_avg_pm10 DESC;


-- 4. Top 3 najbardziej zanieczyszczone godziny w każdym mieście (CTE + Window Function)
WITH ranked_hours AS (
    SELECT
        city,
        time,
        pm10,
        pm2_5,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY pm10 DESC) AS rn
    FROM measurements
    WHERE pm10 IS NOT NULL
)
SELECT
    city,
    time,
    pm10,
    pm2_5
FROM ranked_hours
WHERE rn <= 3
ORDER BY city, pm10 DESC;
