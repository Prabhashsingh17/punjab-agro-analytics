-- ============================================================
-- PUNJAB AGRO CENTRE - Sales Analytics SQL Queries
-- Location: Gopalganj, Bihar | Agricultural Equipment Sales
-- Fresher Data Analyst Portfolio Project
-- ============================================================

-- Tables: customers, sales, inventory
-- Import CSV files into SQLite/MySQL/PostgreSQL before running

-- ------------------------------------------------------------
-- Q1: Total Revenue & Units Sold (Overall KPIs)
-- ------------------------------------------------------------
SELECT
    COUNT(DISTINCT sale_id)       AS total_orders,
    SUM(quantity)                 AS total_units_sold,
    ROUND(SUM(net_revenue), 2)    AS total_revenue_inr,
    ROUND(AVG(net_revenue), 2)    AS avg_order_value_inr
FROM sales
WHERE delivery_status = 'Delivered';


-- ------------------------------------------------------------
-- Q2: Monthly Revenue Trend (2023 vs 2024)
-- ------------------------------------------------------------
SELECT
    year,
    month,
    COUNT(sale_id)                AS orders,
    SUM(quantity)                 AS units,
    ROUND(SUM(net_revenue), 2)    AS monthly_revenue
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY year, month
ORDER BY year, month;


-- ------------------------------------------------------------
-- Q3: Top Selling Equipment by Revenue
-- ------------------------------------------------------------
SELECT
    equipment,
    COUNT(sale_id)                AS total_orders,
    SUM(quantity)                 AS units_sold,
    ROUND(SUM(net_revenue), 2)    AS total_revenue,
    ROUND(AVG(unit_price), 2)     AS avg_unit_price
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY equipment
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------
-- Q4: District-wise Sales (Bihar districts coming to Gopalganj)
-- ------------------------------------------------------------
SELECT
    district,
    COUNT(DISTINCT customer_id)   AS unique_customers,
    COUNT(sale_id)                AS total_orders,
    ROUND(SUM(net_revenue), 2)    AS district_revenue,
    ROUND(
        100.0 * SUM(net_revenue) / (SELECT SUM(net_revenue) FROM sales WHERE delivery_status = 'Delivered'),
        2
    ) AS revenue_share_pct
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY district
ORDER BY district_revenue DESC;


-- ------------------------------------------------------------
-- Q5: Seasonal Demand Analysis (Kharif vs Rabi)
-- ------------------------------------------------------------
SELECT
    season,
    equipment,
    SUM(quantity)                 AS units_sold,
    ROUND(SUM(net_revenue), 2)    AS season_revenue
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY season, equipment
ORDER BY season, season_revenue DESC;


-- ------------------------------------------------------------
-- Q6: Customer Type Breakdown (Farmer vs Dealer vs Cooperative)
-- ------------------------------------------------------------
SELECT
    customer_type,
    COUNT(DISTINCT customer_id)   AS customers,
    COUNT(sale_id)                AS orders,
    ROUND(SUM(net_revenue), 2)    AS revenue,
    ROUND(AVG(net_revenue), 2)    AS avg_order_value
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY customer_type
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- Q7: Payment Mode Preference
-- ------------------------------------------------------------
SELECT
    payment_mode,
    COUNT(sale_id)                AS transactions,
    ROUND(SUM(net_revenue), 2)    AS revenue,
    ROUND(100.0 * COUNT(sale_id) / (SELECT COUNT(*) FROM sales WHERE delivery_status = 'Delivered'), 2) AS txn_share_pct
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY payment_mode
ORDER BY transactions DESC;


-- ------------------------------------------------------------
-- Q8: Top 10 Customers by Lifetime Value
-- ------------------------------------------------------------
SELECT
    s.customer_id,
    c.customer_name,
    c.district,
    c.customer_type,
    COUNT(s.sale_id)              AS total_purchases,
    ROUND(SUM(s.net_revenue), 2)  AS lifetime_value
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
WHERE s.delivery_status = 'Delivered'
GROUP BY s.customer_id, c.customer_name, c.district, c.customer_type
ORDER BY lifetime_value DESC
LIMIT 10;


-- ------------------------------------------------------------
-- Q9: Discount Impact Analysis
-- ------------------------------------------------------------
SELECT
    discount_pct,
    COUNT(sale_id)                AS orders,
    ROUND(AVG(net_revenue), 2)    AS avg_revenue,
    ROUND(SUM(net_revenue), 2)    AS total_revenue
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY discount_pct
ORDER BY discount_pct;


-- ------------------------------------------------------------
-- Q10: Year-over-Year Growth by Equipment
-- ------------------------------------------------------------
SELECT
    equipment,
    SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END) AS revenue_2023,
    SUM(CASE WHEN year = 2024 THEN net_revenue ELSE 0 END) AS revenue_2024,
    ROUND(
        100.0 * (
            SUM(CASE WHEN year = 2024 THEN net_revenue ELSE 0 END) -
            SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END)
        ) / NULLIF(SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END), 0),
        2
    ) AS yoy_growth_pct
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY equipment
ORDER BY yoy_growth_pct DESC;
