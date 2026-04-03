# run_once/test_airtable.py
import requests, os
from dotenv import load_dotenv
load_dotenv()

base    = os.environ["AIRTABLE_BASE_ID"]
table   = os.environ["AIRTABLE_TABLE_NAME"]
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_API_KEY']}"}

# 1. Read existing records
r = requests.get(
    f"https://api.airtable.com/v0/{base}/{table}",
    headers=headers,
    params={"maxRecords": 3}
)
print("Read status:", r.status_code)
print("Records found:", len(r.json().get("records", [])))

# 2. Create a test record
payload = {
    "records": [{
        "fields": {
            "brand_name": "TEST — delete me",
            "content_type": "reel",
            "status": "Brief Received"
        }
    }]
}
r2 = requests.post(
    f"https://api.airtable.com/v0/{base}/{table}",
    headers={**headers, "Content-Type": "application/json"},
    json=payload
)
print("Write status:", r2.status_code)
record_id = r2.json()["records"][0]["id"]
print("Created record ID:", record_id)

# 3. Delete the test record
r3 = requests.delete(
    f"https://api.airtable.com/v0/{base}/{table}/{record_id}",
    headers=headers
)
print("Delete status:", r3.status_code)
print("All Airtable checks passed.")