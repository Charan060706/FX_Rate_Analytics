import csv

data = """currency_code,currency_name,region,is_major
USD,US Dollar,Americas,true
EUR,Euro,Europe,true
GBP,British Pound,Europe,true
JPY,Japanese Yen,Asia,true
INR,Indian Rupee,Asia,false
CNY,Chinese Yuan,Asia,false
CHF,Swiss Franc,Europe,true
AUD,Australian Dollar,Oceania,true
CAD,Canadian Dollar,Americas,true
BRL,Brazilian Real,Americas,false
ZAR,South African Rand,Africa,false
TRY,Turkish Lira,Middle East,false
SGD,Singapore Dollar,Asia,true
"""

with open("dim_currency.csv", "w", newline="", encoding="utf-8") as file:
    file.write(data)

print("currencies.csv created successfully!")