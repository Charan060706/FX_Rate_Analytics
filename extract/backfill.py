import datetime
import requests
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "currency-tracker-507607"
TABLE_ID = f"{PROJECT_ID}.fx_raw.exchange_rates_raw"
TARGET_CURRENCIES = "EUR,GBP,JPY,INR,CNY,CHF,AUD,CAD,BRL,ZAR,TRY,SGD"

