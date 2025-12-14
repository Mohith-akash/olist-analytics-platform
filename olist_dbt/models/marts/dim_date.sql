{{
    config(
        materialized='table'
    )
}}

with date_spine as (
    {{ dbt_date.get_date_dimension('2016-01-01', '2019-01-01') }}
)

select * from date_spine
