{{config(materialized = 'table')}}

with returns as (
    select * from {{ref('fct_fx_daily_returns')}}
)

select
  date,base,target,rate,daily_return_pct,
  round(STDDEV(daily_return_pct) over(
    PARTITION BY base,target
    order by date 
    rows between 6 preceding and current row
  ),4) as rolling_volataility_7d,

  round(stddev(daily_return_pct) over (
        partition by base, target
        order by date
        rows between 29 preceding and current row
    ), 4) as rolling_volatility_30d

from returns