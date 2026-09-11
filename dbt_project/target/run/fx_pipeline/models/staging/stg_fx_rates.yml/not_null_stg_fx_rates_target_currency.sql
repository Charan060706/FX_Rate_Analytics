
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select target_currency
from `currency-tracker-507607`.`fx_marts`.`stg_fx_rates`
where target_currency is null



  
  
      
    ) dbt_internal_test