

with date_spine as(
    select day_date from 
    unnest(generate_date_array('2021-01-01', '2030-12-31', interval 1 day)) as day_date
)

select 
   day_date as date, 
   extract(year from day_date) as year, 
   extract(quarter from day_date) as quarter,
   extract(month from day_date) as month,  
   format_date('%B',day_date) as month_name,
   extract(day from day_date) as day_of_month, 
   extract(dayofweek from day_date) as day_of_week, 
   format_date('%A',day_date) as day_name,
   case
      when extract(dayofweek from day_date) in (1,7) then true
      else false
    end as is_weekend

from date_spine