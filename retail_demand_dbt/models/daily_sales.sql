{{ config(materialized='view') }}

SELECT
    item_id,
    dept_id,
    cat_id,
    store_id,
    state_id,
    day,
    sales
FROM {{ ref('stg_sales_train') }}
UNPIVOT (
    sales FOR day IN (
        d_1, d_2, d_3, d_4, d_5,
        d_6, d_7, d_8, d_9, d_10
    )
)