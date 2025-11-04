-- Task 3: Daily total amount of sales from orders
SELECT
    DATE(order_date) AS order_day,
    SUM(total_amount) AS daily_sales
FROM orders
GROUP BY order_day
ORDER BY order_day;
