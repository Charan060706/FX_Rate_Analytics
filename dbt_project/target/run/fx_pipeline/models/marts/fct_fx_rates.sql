-- back compat for old kwarg name
  
  
        
            
                
                
            
                
                
            
                
                
            
        
    

    

    merge into `currency-tracker-507607`.`fx_marts`.`fct_fx_rates` as DBT_INTERNAL_DEST
        using (

select rate_date as date,base_currency as base,target_currency as target,exchange_rate as rate,
loaded_at from `currency-tracker-507607`.`fx_marts`.`stg_fx_rates`


    where rate_date > (select max(date) from `currency-tracker-507607`.`fx_marts`.`fct_fx_rates`)

        ) as DBT_INTERNAL_SOURCE
        on (
                    DBT_INTERNAL_SOURCE.date = DBT_INTERNAL_DEST.date
                ) and (
                    DBT_INTERNAL_SOURCE.base = DBT_INTERNAL_DEST.base
                ) and (
                    DBT_INTERNAL_SOURCE.target = DBT_INTERNAL_DEST.target
                )

    
    when matched then update set
        `date` = DBT_INTERNAL_SOURCE.`date`,`base` = DBT_INTERNAL_SOURCE.`base`,`target` = DBT_INTERNAL_SOURCE.`target`,`rate` = DBT_INTERNAL_SOURCE.`rate`,`loaded_at` = DBT_INTERNAL_SOURCE.`loaded_at`
    

    when not matched then insert
        (`date`, `base`, `target`, `rate`, `loaded_at`)
    values
        (`date`, `base`, `target`, `rate`, `loaded_at`)


    