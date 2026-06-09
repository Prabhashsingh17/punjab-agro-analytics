-- ============================================================
-- PUNJAB AGRO CENTRE — BUSINESS ANALYTICS SQL QUERIES
-- Data Analytics + Business Intelligence
-- Descriptive | Diagnostic | Prescriptive
-- ============================================================

-- ------------------------------------------------------------
-- BA1: Executive KPI Scorecard (Descriptive Analytics)
-- ------------------------------------------------------------
SELECT
    ROUND(SUM(net_revenue), 0)              AS total_revenue,
    COUNT(DISTINCT sale_id)                 AS total_orders,
    COUNT(DISTINCT customer_id)             AS active_customers,
    COUNT(DISTINCT district)                AS districts_served,
    ROUND(AVG(net_revenue), 0)              AS avg_order_value,
    ROUND(SUM(quantity), 0)                 AS units_sold
FROM sales
WHERE delivery_status = 'Delivered';


-- ------------------------------------------------------------
-- BA2: Customer Segmentation by Lifetime Value (Diagnostic)
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN lifetime_value >= 300000 THEN 'High Value'
        WHEN lifetime_value >= 100000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*)                          AS customers,
    ROUND(AVG(lifetime_value), 0)     AS avg_lifetime_value,
    ROUND(SUM(lifetime_value), 0)     AS segment_revenue
FROM (
    SELECT customer_id, SUM(net_revenue) AS lifetime_value
    FROM sales WHERE delivery_status = 'Delivered'
    GROUP BY customer_id
) t
GROUP BY customer_segment
ORDER BY segment_revenue DESC;


-- ------------------------------------------------------------
-- BA3: Profit Margin Analysis by Equipment (Diagnostic)
-- ------------------------------------------------------------
SELECT
    s.equipment,
    ROUND(SUM(s.net_revenue), 0)                              AS revenue,
    ROUND(SUM((s.unit_price - i.avg_unit_cost) * s.quantity), 0) AS estimated_profit,
    ROUND(
        100.0 * SUM((s.unit_price - i.avg_unit_cost) * s.quantity) / SUM(s.net_revenue), 1
    ) AS profit_margin_pct
FROM sales s
JOIN inventory i ON s.equipment = i.equipment
WHERE s.delivery_status = 'Delivered'
GROUP BY s.equipment
ORDER BY estimated_profit DESC;


-- ------------------------------------------------------------
-- BA4: Inventory Turnover & Stock Health (Business Ops)
-- ------------------------------------------------------------
SELECT
    i.equipment,
    i.stock_quantity,
    i.reorder_level,
    COALESCE(SUM(s.quantity), 0)          AS units_sold,
    ROUND(COALESCE(SUM(s.quantity), 0) * 1.0 / i.stock_quantity, 2) AS turnover_ratio,
    CASE
        WHEN i.stock_quantity <= i.reorder_level THEN 'REORDER NOW'
        ELSE 'Healthy'
    END AS stock_status
FROM inventory i
LEFT JOIN sales s ON i.equipment = s.equipment AND s.delivery_status = 'Delivered'
GROUP BY i.equipment, i.stock_quantity, i.reorder_level
ORDER BY turnover_ratio DESC;


-- ------------------------------------------------------------
-- BA5: Market Share by District (Geographic Business Analysis)
-- ------------------------------------------------------------
SELECT
    district,
    ROUND(SUM(net_revenue), 0)            AS district_revenue,
    ROUND(100.0 * SUM(net_revenue) /
        (SELECT SUM(net_revenue) FROM sales WHERE delivery_status = 'Delivered'), 1
    ) AS market_share_pct,
    COUNT(DISTINCT customer_id)           AS customers
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY district
ORDER BY district_revenue DESC;


-- ------------------------------------------------------------
-- BA6: Customer Type Revenue Contribution (Business Mix)
-- ------------------------------------------------------------
SELECT
    customer_type,
    COUNT(DISTINCT customer_id)           AS customers,
    COUNT(sale_id)                        AS orders,
    ROUND(SUM(net_revenue), 0)            AS revenue,
    ROUND(100.0 * SUM(net_revenue) /
        (SELECT SUM(net_revenue) FROM sales WHERE delivery_status = 'Delivered'), 1
    ) AS revenue_share_pct,
    ROUND(AVG(net_revenue), 0)             AS avg_order_value
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY customer_type
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- BA7: Seasonal Business Planning (Prescriptive Input)
-- ------------------------------------------------------------
SELECT
    season,
    equipment,
    SUM(quantity)                         AS units,
    ROUND(SUM(net_revenue), 0)            AS revenue,
    ROUND(AVG(net_revenue), 0)             AS avg_deal_size
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY season, equipment
ORDER BY season, revenue DESC;


-- ------------------------------------------------------------
-- BA8: Year-over-Year Business Growth (Trend Analysis)
-- ------------------------------------------------------------
SELECT
    equipment,
    ROUND(SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END), 0) AS rev_2023,
    ROUND(SUM(CASE WHEN year = 2024 THEN net_revenue ELSE 0 END), 0) AS rev_2024,
    ROUND(
        100.0 * (
            SUM(CASE WHEN year = 2024 THEN net_revenue ELSE 0 END) -
            SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END)
        ) / NULLIF(SUM(CASE WHEN year = 2023 THEN net_revenue ELSE 0 END), 0), 1
    ) AS yoy_growth_pct
FROM sales
WHERE delivery_status = 'Delivered'
GROUP BY equipment
ORDER BY yoy_growth_pct DESC;
