with source as (
    select * from {{ source('raw_olist', 'products') }}
),

translation as (
    select * from {{ source('raw_olist', 'category_translation') }}
),

renamed as (
    select
        p.product_id,
        -- Use English name if available, fallback to Portuguese
        coalesce(t.product_category_name_english, p.product_category_name) as product_category_name,
        p.product_name_lenght,
        p.product_description_lenght,
        p.product_photos_qty,
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm
    from source p
    left join translation t
        on p.product_category_name = t.product_category_name
)

select * from renamed