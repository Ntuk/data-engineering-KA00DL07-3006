-- Task 08a – GA4 Daily User Data Query
CREATE OR REPLACE TABLE `oamk-476515.G4_daily_user.G4_daily_user_data` AS
SELECT
  user_pseudo_id,
  COUNT(event_name) AS event_count,
  SUM(ecommerce.purchase_revenue_in_usd) AS total_revenue
FROM
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20210115' AND '20210131'
GROUP BY
  user_pseudo_id
ORDER BY
  total_revenue DESC;

-- Task 08b – Query GA4 ecommerce data (15.1–31.1, 2021)
SELECT
  user_pseudo_id,
  COUNT(event_name) AS event_count,
  SUM(
    COALESCE(
      (SELECT ep.value.int_value
       FROM UNNEST(event_params) AS ep
       WHERE ep.key = 'value'),
      0)
  ) AS total_revenue
FROM
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20210101' AND '20210131'
  AND event_name = 'purchase'
GROUP BY
  user_pseudo_id
ORDER BY
  total_revenue DESC;

-- Task 08c – Query data from BigQuery table for local pandas import
SELECT
  *
FROM
  `oamk-476515.G4_daily_user.G4_daily_user_data`
ORDER BY
  total_revenue DESC;
  