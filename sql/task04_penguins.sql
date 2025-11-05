-- Task 4: Calculate average body mass, culmen length, and culmen depth grouped by island and sex.
SELECT
  island,
  sex,
  AVG(body_mass_g) AS avg_body_mass_g,
  AVG(culmen_length_mm) AS avg_culmen_length_mm,
  AVG(culmen_depth_mm) AS avg_culmen_depth_mm
FROM `bigquery-public-data.ml_datasets.penguins`
WHERE sex IS NOT NULL
GROUP BY island, sex
ORDER BY island, sex;
