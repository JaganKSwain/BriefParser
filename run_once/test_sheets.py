# run_once/test_sheets.py
# Verifies Sheets connectivity AND prints the detected column headers.
# Run this to confirm your Google Form question labels match HEADER_MAP.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_JSON
from tools.sheets import fetch_new_briefs, HEADER_MAP

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly"
]

creds   = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_JSON, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

# --- 1. Detect sheet name ---
meta       = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
sheet_name = meta["sheets"][0]["properties"]["title"]
print(f"Sheet name: '{sheet_name}'")

# --- 2. Read first 5 rows ---
result = service.spreadsheets().values().get(
    spreadsheetId=GOOGLE_SHEET_ID,
    range=f"{sheet_name}!A1:Z5"
).execute()
rows = result.get("values", [])
print(f"Rows found (including header): {len(rows)}")

if rows:
    print("\nHeader row (your Google Form question labels):")
    for i, h in enumerate(rows[0]):
        normalised = h.strip().lower()
        mapped     = HEADER_MAP.get(normalised, "⚠️  NOT IN HEADER_MAP")
        print(f"  Col {i}: '{h}'  →  {mapped}")

    if len(rows) > 1:
        print(f"\nSample data rows: {len(rows)-1}")
        for row in rows[1:]:
            print(f"  {row}")

# --- 3. Test fetch_new_briefs ---
print("\n--- fetch_new_briefs() ---")
briefs = fetch_new_briefs()
print(f"New (unprocessed) briefs: {len(briefs)}")
for b in briefs:
    print(f"  {b.row_id}: {b.brand_name} / {b.content_type} / {b.topic}")