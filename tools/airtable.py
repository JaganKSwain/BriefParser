import requests
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME
from datetime import date


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type":  "application/json"
    }


def create_brief_record(
    brand_name: str,
    content_type: str,
    topic: str,
    status: str,
    scriptwriter: str,
    notion_link: str,
    flag_reason: str
) -> str:
    """Creates a new record. Returns the Airtable record ID."""

    payload = {
        "records": [{
            "fields": {
                "brand_name":   brand_name,
                "content_type": content_type,
                "topic":        topic,
                "status":       status,
                "scriptwriter": scriptwriter,
                "notion_link":  notion_link,
                "submitted_at": date.today().isoformat(),
                "processed_at": date.today().isoformat(),
                "flag_reason":  flag_reason
            }
        }]
    }

    r = requests.post(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}",
        headers=_headers(),
        json=payload,
        timeout=10
    )
    r.raise_for_status()
    return r.json()["records"][0]["id"]


def update_record_status(record_id: str, status: str, extra_fields: dict = None):
    """Updates an existing record's status and any additional fields."""

    fields = {"status": status}
    if extra_fields:
        fields.update(extra_fields)

    payload = {"fields": fields}

    r = requests.patch(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}/{record_id}",
        headers=_headers(),
        json=payload,
        timeout=10
    )
    r.raise_for_status()
    return r.json()


def get_record(record_id: str) -> dict:
    """Fetches a single record by ID."""
    r = requests.get(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}/{record_id}",
        headers=_headers(),
        timeout=10
    )
    r.raise_for_status()
    return r.json()