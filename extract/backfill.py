import datetime
import requests
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "currency-tracker-507607"
TABLE_ID = f"{PROJECT_ID}.fx_raw.exchange_rates_raw"
TARGET_CURRENCIES = "EUR,GBP,JPY,INR,CNY,CHF,AUD,CAD,BRL,ZAR,TRY,SGD"

def run_backfill():
    start_date = '2021-01-01'

    end_date = datetime.date.today().strftime("%Y-%m-%d")

    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from=USD&to={TARGET_CURRENCIES}"

    print(f"Fetching historical rates from {start_date} to {end_date}...")

    response = requests.get(url,timeout=60)

    response.raise_for_status()

    data = response.json()

    rows = []

    loaded_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for date_str,rates in data.get("rates",{}).items():
        for curr,rate in rates.items():
            rows.append({
                "date": date_str,
                "base": "USD",
                "target": curr,
                "rate": float(rate),
                "loaded_at": loaded_at
            })


    df = pd.DataFrame(rows)

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["loaded_at"] = pd.to_datetime(df["loaded_at"])

    print(f"Transformed {len(df)} rows. Writing to BigQuery...")

    client = bigquery.Client(project=PROJECT_ID)
    job_config = bigquery.LoadJobConfig(
        write_disposition  = bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema = [
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("base", "STRING"),
            bigquery.SchemaField("target", "STRING"),
            bigquery.SchemaField("rate", "FLOAT64"),
            bigquery.SchemaField("loaded_at", "TIMESTAMP"),
        ]
    )

    job = client.load_table_from_dataframe(df,TABLE_ID,job_config=job_config)

    job.result()
    print(f"Success! Populated {TABLE_ID} with {len(df)} records.")


if __name__=="__main__":
    run_backfill()
