# tools/test_tools.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from schemas import RawBrief, InterpretedBrief
from tools.sheets import fetch_new_briefs
from tools.notion import create_brief_page
from tools.slack import notify_scriptwriter, notify_error
from tools.airtable import create_brief_record, update_record_status, get_record
from datetime import date, timedelta

print("\n--- Sheets ---")
briefs = fetch_new_briefs()
print(f"New briefs found: {len(briefs)}")
for b in briefs:
    print(f"  {b.row_id}: {b.brand_name} / {b.content_type}")

print("\n--- Notion (clean brief) ---")
raw = RawBrief(
    row_id="test_001",
    brand_name="GlowSkin",
    content_type="reel",
    topic="SPF myths",
    key_message="SPF is not just for summer",
    target_audience="Women 25-40",
    mandatory_inclusions="Mention dermatologist tested",
    reference_urls="",
    free_text_notes=""
)
interpreted = InterpretedBrief(
    hook_options=[
        "You're wearing SPF wrong — here's what dermatologists actually recommend",
        "The one skincare step 80% of people skip in winter",
        "SPF myth that's ageing your skin faster than you think"
    ],
    tone_direction="Warm and educational, conversational with a light urgency",
    visual_treatment="Close-up skincare routine shots, text overlays for stats",
    scriptwriter_notes="Open with a surprising stat. Reference dermatologist tested in first 10 seconds.",
    one_line_summary="Debunking SPF myths for daily skincare routines",
    ambiguity_flags=[],
    confidence_score=0.91
)
notion_url = create_brief_page(raw, interpreted, flagged=False)
print(f"Notion page: {notion_url}")

print("\n--- Notion (flagged brief) ---")
flag_url = create_brief_page(
    raw,
    flagged=True,
    flag_reason="Missing key_message and target_audience"
)
print(f"Flagged page: {flag_url}")

print("\n--- Slack (clean) ---")
deadline = (date.today() + timedelta(days=2)).strftime("%d %b %Y")
ok = notify_scriptwriter(
    scriptwriter_name="Riya Sharma",
    brand_name="GlowSkin",
    content_type="reel",
    one_line_summary="Debunking SPF myths for daily skincare routines",
    notion_url=notion_url,
    deadline=deadline,
    flagged=False
)
print(f"Slack clean notify: {ok}")

print("\n--- Slack (flagged) ---")
ok2 = notify_scriptwriter(
    scriptwriter_name="",
    brand_name="GlowSkin",
    content_type="reel",
    one_line_summary="",
    notion_url=flag_url,
    deadline=deadline,
    flagged=True,
    flag_reason="Missing key_message and target_audience"
)
print(f"Slack flag notify: {ok2}")

print("\n--- Slack (error alert) ---")
ok3 = notify_error("Airtable write", "Connection timeout after 3 retries")
print(f"Slack error notify: {ok3}")

print("\n--- Airtable (create) ---")
record_id = create_brief_record(
    brand_name="GlowSkin",
    content_type="reel",
    topic="SPF myths",
    status="Brief Processed",
    scriptwriter="Riya Sharma",
    notion_link=notion_url,
    flag_reason=""
)
print(f"Created record: {record_id}")

print("\n--- Airtable (update) ---")
update_record_status(record_id, "Brief Processed", {"scriptwriter": "Riya Sharma"})
print("Status updated")

print("\n--- Airtable (fetch) ---")
rec = get_record(record_id)
print(f"Fetched: {rec['fields']['brand_name']} — {rec['fields']['status']}")

print("\nAll tools verified.")