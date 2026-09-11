import datetime
import requests
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "currency-tracker-507607"
TABLE_ID = f"{PROJECT_ID}.fx_raw.exchange_rates_raw"
TARGET_CURRENCIES = "EUR,GBP,JPY,INR,CNY,CHF,AUD,CAD,BRL,ZAR,TRY,SGD"

def run_incremental():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"SELECT MAX(date) as max_date FROM {TABLE_ID}"

    result = client.query(query).to_dataframe()

    max_date = result["max_date"].iloc[0]

    if pd.isnull(max_date):
        raise ValueError("Raw table is empty. Please run backfill.py first.")

    start_date = max_date + datetime.timedelta(days=1)

    today = datetime.date.today()

    if start_date > today:
        print("Data is already up to date.")
        return

    url = f"https://api.frankfurter.app/{start_date}..{today}?from=USD&to={TARGET_CURRENCIES}"
    res = requests.get(url, timeout=30)

    if res.status_code == 404 or not res.json().get("rates"):
        print(f"No new rates available between {start_date} and {today} (weekend or ECB holiday).")
        return

    res.raise_for_status()

    data = res.json()

    rows = []

    loaded_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for date_str,rates in data.get("rates", {}).items():
        for curr,rate in rates.items():
            rows.append({
                "date": date_str,
                "base": "USD",
                "target": curr,
                "rate": float(rate),
                "loaded_at": loaded_at
            })

    if not rows:
        print("No new records to insert.")
        return

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["loaded_at"] = pd.to_datetime(df["loaded_at"])

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)

    client.load_table_from_dataframe(df,TABLE_ID,job_config=job_config).result()

    print(f"Successfully appended {len(df)} new records.")


if __name__ == "__main__":
    run_incremental()


    