with raw_source as (
    select 
    cast(date as date) as rate_Date,
    cast(base as string) as base_currency,
    cast(target as string) as target_currency,
    cast(rate as float64) as exchange_rate,
    cast(loaded_at as timestamp) as loaded_at,
    ROW_NUMBER() over(
        PARTITION BY date,base,target
        order by loaded_at DESC 
    ) as dedupe_rank

    from `currency-tracker-507607`.`fx_raw`.`exchange_rates_raw`
)

select rate_Date,base_currency,target_currency,exchange_rate,loaded_at from raw_source 
where dedupe_rank = 1