
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select target
from `currency-tracker-507607`.`fx_marts`.`fct_fx_rates`
where target is null



  
  
      
    ) dbt_internal_test