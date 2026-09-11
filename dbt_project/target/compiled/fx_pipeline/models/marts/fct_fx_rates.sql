

select rate_date as date,base_currency as base,target_currency as target,exchange_rate as rate,
loaded_at from `currency-tracker-507607`.`fx_marts`.`stg_fx_rates`


    where rate_date > (select max(date) from `currency-tracker-507607`.`fx_marts`.`fct_fx_rates`)
