with source as (

    select * from {{ source('raw_olist', 'order_items') }}

),

renamed as (

    select
        order_id,
        order_item_id as item_sequence_number,
        product_id,
        seller_id,
        price,
        freight_value
    from source

)

select * from renamed