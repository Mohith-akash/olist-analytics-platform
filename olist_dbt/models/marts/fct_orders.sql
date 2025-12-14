with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

final as (

    select
        -- Key IDs
        order_items.order_id,
        orders.customer_id,
        order_items.product_id,
        
        -- Time details
        orders.order_purchase_timestamp,
        
        -- Product details
        products.product_category_name,
        
        -- Financials
        order_items.price,
        order_items.freight_value,
        (order_items.price + order_items.freight_value) as total_order_value

    from order_items
    
    left join orders 
        on order_items.order_id = orders.order_id
        
    left join products 
        on order_items.product_id = products.product_id

)

select * from final