{{
    config(
        materialized='table'
    )
}}

with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

-- Pre-aggregate metrics (avoid fan-out in final join)
product_sales as (
    select
        product_id,
        count(*) as times_sold,
        sum(price) as total_revenue,
        sum(freight_value) as total_freight,
        avg(price) as avg_selling_price
    from order_items
    group by product_id
),

final as (
    select
        -- Identifiers
        p.product_id,
        
        -- Details
        p.product_category_name,
        
        -- Dimensions
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm,
        
        -- Calculated volume
        (p.product_length_cm * p.product_height_cm * p.product_width_cm) as volume_cm3,
        
        -- Metrics
        coalesce(ps.times_sold, 0) as times_sold,
        coalesce(ps.total_revenue, 0) as total_revenue,
        coalesce(ps.total_freight, 0) as total_freight,
        coalesce(ps.avg_selling_price, 0) as avg_selling_price,
        
        -- Sales Tiering
        case
            when ps.times_sold >= 50 then 'High Seller'
            when ps.times_sold >= 10 then 'Medium Seller'
            when ps.times_sold >= 1 then 'Low Seller'
            else 'Never Sold'
        end as sales_tier

    from products p
    left join product_sales ps on p.product_id = ps.product_id
)

select * from final
