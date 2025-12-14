{{
    config(
        materialized='table'
    )
}}

with sellers as (
    select * from {{ ref('stg_sellers') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

reviews as (
    select * from {{ ref('stg_reviews') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- Join path: items -> orders -> reviews
seller_reviews as (
    select
        oi.seller_id,
        avg(r.review_score) as avg_review_score,
        count(r.review_id) as total_reviews
    from order_items oi
    inner join orders o on oi.order_id = o.order_id
    inner join reviews r on o.order_id = r.order_id
    group by oi.seller_id
),

-- Aggregate seller sales metrics
seller_sales as (
    select
        seller_id,
        count(distinct order_id) as total_orders,
        sum(price) as total_revenue,
        sum(freight_value) as total_freight,
        avg(price) as avg_item_price
    from order_items
    group by seller_id
),

final as (
    select
        -- Seller identifiers
        s.seller_id,
        
        -- Location
        s.zip_code,
        s.city,
        s.state,
        
        -- Sales metrics
        coalesce(ss.total_orders, 0) as total_orders,
        coalesce(ss.total_revenue, 0) as total_revenue,
        coalesce(ss.total_freight, 0) as total_freight,
        coalesce(ss.avg_item_price, 0) as avg_item_price,
        
        -- Review metrics
        round(coalesce(sr.avg_review_score, 0), 2) as avg_review_score,
        coalesce(sr.total_reviews, 0) as total_reviews,
        
        -- Seller tier based on revenue
        case
            when ss.total_revenue >= 50000 then 'Platinum'
            when ss.total_revenue >= 10000 then 'Gold'
            when ss.total_revenue >= 1000 then 'Silver'
            else 'Bronze'
        end as seller_tier

    from sellers s
    left join seller_sales ss on s.seller_id = ss.seller_id
    left join seller_reviews sr on s.seller_id = sr.seller_id
)

select * from final
