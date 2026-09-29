{{ config(materialized='view') }}

SELECT
    item_id,
    dept_id,
    cat_id,
    SUM(d_1 + d_2 + d_3 + d_4 + d_5 + d_6 + d_7 + d_8 + d_9 + d_10) AS total_sales_10_days,
    AVG(d_1 + d_2 + d_3 + d_4 + d_5 + d_6 + d_7 + d_8 + d_9 + d_10) AS avg_sales_10_days
FROM {{ ref('stg_sales_train') }}
GROUP BY
    item_id,
    dept_id,
    cat_id