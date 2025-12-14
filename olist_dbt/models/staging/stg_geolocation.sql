with source as (
    select * from {{ source('raw_olist', 'geolocation') }}
),

-- Aggregate so we have unique lat/long per zip code
aggregated as (
    select
        geolocation_zip_code_prefix as zip_code,
        -- Take the average coordinate to center the zip code
        avg(geolocation_lat) as geolocation_lat,
        avg(geolocation_lng) as geolocation_lng,
        -- Use the most common state/city for this zip
        max(geolocation_city) as city,
        max(geolocation_state) as state
    from source
    group by geolocation_zip_code_prefix
)

select * from aggregated
