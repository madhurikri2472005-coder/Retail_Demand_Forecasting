{{ config(materialized='view') }}

SELECT
    item_id,
    dept_id,
    cat_id,
    store_id,
    state_id,
    day,
    sales
FROM {{ ref('daily_sales') }}
WHERE sales >= 0