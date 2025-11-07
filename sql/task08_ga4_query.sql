-- Task 08 – GA4 Daily User Data Query
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
