
  
    

    create or replace table `currency-tracker-507607`.`fx_marts`.`fct_fx_daily_returns`
      
    
    

    
    OPTIONS()
    as (
      

with base_rates as (
    select date,base,target,rate,
    lag(rate) over(
        PARTITION by base,target
        order by date 
    ) as prev_rate 

    from `currency-tracker-507607`.`fx_marts`.`fct_fx_rates`
)

select 
  date,
  base,target,rate,prev_rate,
  case 
     when prev_rate is null then 0.0
     else round(((rate-prev_rate)/prev_rate)*100 , 4)

  end as daily_return_pct

from base_rates
    );
  