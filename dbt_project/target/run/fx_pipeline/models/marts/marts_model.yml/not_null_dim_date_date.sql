
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date
from `currency-tracker-507607`.`fx_marts`.`dim_date`
where date is null



  
  
      
    ) dbt_internal_test