{{
    config(
        materialized='table'
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

-- Calculate LTV and order counts
customer_orders as (
    select
        o.customer_id,
        count(distinct o.order_id) as total_orders,
        min(o.order_purchase_timestamp) as first_order_date,
        max(o.order_purchase_timestamp) as last_order_date,
        sum(oi.price) as total_revenue,
        sum(oi.freight_value) as total_freight_paid,
        avg(oi.price) as avg_order_value
    from orders o
    left join order_items oi on o.order_id = oi.order_id
    group by o.customer_id
),

final as (
    select
        -- Identifiers
        c.customer_id,
        c.customer_unique_id,
        
        -- Location
        c.zip_code,
        c.city,
        c.state,
        
        -- Order Metrics
        coalesce(co.total_orders, 0) as total_orders,
        co.first_order_date,
        co.last_order_date,
        
        -- Financials
        coalesce(co.total_revenue, 0) as lifetime_value,
        coalesce(co.total_freight_paid, 0) as total_freight_paid,
        coalesce(co.avg_order_value, 0) as avg_order_value,
        
        -- Segmentation
        case
            when co.total_orders > 1 then 'Returning'
            when co.total_orders = 1 then 'One-time'
            else 'No Orders'
        end as customer_type

    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final
