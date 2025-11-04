-- Task 2b: Join employee_projects and employees_realistic
SELECT 
    ep.project_id,
    ep.employee_id,
    ep.hours_worked,
    er.salary
FROM employee_projects AS ep
JOIN employees_realistic AS er
    ON ep.employee_id = er.employee_id;


-- Task 2c: Calculate total salary costs per project
SELECT
    ep.project_id,
    SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
FROM employee_projects AS ep
JOIN employees_realistic AS er
    ON ep.employee_id = er.employee_id
GROUP BY ep.project_id;


-- Task 2d: Join salary costs per project with project budgets
SELECT
    p.project_id,
    p.budget,
    sc.salary_costs
FROM projects AS p
JOIN (
    SELECT
        ep.project_id,
        SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
    FROM employee_projects AS ep
    JOIN employees_realistic AS er
        ON ep.employee_id = er.employee_id
    GROUP BY ep.project_id
) AS sc
    ON p.project_id = sc.project_id;


-- Task 2e: Calculate salary cost fraction of project budget
SELECT
    p.project_id,
    p.budget,
    sc.salary_costs,
    ROUND((sc.salary_costs / p.budget) * 100, 2) AS salary_cost_percent
FROM projects AS p
JOIN (
    SELECT
        ep.project_id,
        SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
    FROM employee_projects AS ep
    JOIN employees_realistic AS er
        ON ep.employee_id = er.employee_id
    GROUP BY ep.project_id
) AS sc
    ON p.project_id = sc.project_id
ORDER BY salary_cost_percent DESC;
