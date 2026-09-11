{{
    config(
        materialized = 'incremental',
        unique_key = ['date','base','target']
    )
}}

select rate_date as date,base_currency as base,target_currency as target,exchange_rate as rate,
loaded_at from {{ref("stg_fx_rates")}}

{% if is_incremental() %}
    where rate_date > (select max(date) from {{this}})
{% endif %}