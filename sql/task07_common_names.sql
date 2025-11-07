-- Task 07 – Most common US names by year
CREATE TABLE `oamk-476515.population_analysis.US_common_names` AS
SELECT
  year,
  gender,
  ANY_VALUE(name) AS name,
  MAX(number) AS total
FROM (
  SELECT
    year,
    gender,
    name,
    number,
    RANK() OVER(PARTITION BY year, gender ORDER BY number DESC) AS rank
  FROM `bigquery-public-data.usa_names.usa_1910_current`
)
WHERE rank = 1
GROUP BY year, gender
ORDER BY year, gender;
