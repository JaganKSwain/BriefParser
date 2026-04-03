from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from schemas import RawBrief
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_JSON
from pathlib import Path
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly"
]

ROOT          = Path(__file__).resolve().parent.parent
PROCESSED_LOG = ROOT / "data" / "processed_rows.json"

# ---------------------------------------------------------------------------
# PRIMARY MAP  — exact Google Form question text (lowercased) → internal field
# "Primary Goal" is the closest proxy for topic (what the content is about).
# "Desired Tone and Style" is the scriptwriter's key creative directive.
# ---------------------------------------------------------------------------
HEADER_MAP: dict[str, str] = {
    # brand_name
    "brand name":                                                   "brand_name",
    "brand":                                                        "brand_name",
    "brand_name":                                                   "brand_name",

    # content_type
    "content type":                                                 "content_type",
    "content_type":                                                 "content_type",
    "format":                                                       "content_type",
    "type of content":                                              "content_type",
    "brief type":                                                   "content_type",

    # topic
    "topic/subject area":                                           "topic",
    "topic":                                                        "topic",
    "content topic":                                                "topic",
    "primary goal of the content (select up to 3)":                 "topic",
    "primary goal of the content":                                  "topic",
    "primary goal":                                                 "topic",
    "objective/scope of work":                                      "topic",
    "project name":                                                 "topic",

    # key_message
    "key message (the one thing the audience must take away)":      "key_message",
    "key message":                                                  "key_message",
    "key_message":                                                  "key_message",
    "core message":                                                 "key_message",
    "main message":                                                 "key_message",

    # target_audience
    "target audience":                                              "target_audience",
    "target_audience":                                              "target_audience",
    "target audience description":                                  "target_audience",
    "audience":                                                     "target_audience",
    "who is this for":                                              "target_audience",
    "client/department":                                            "target_audience",

    # mandatory_inclusions
    "mandatory inclusions (keywords, ctas, product features, compliance text, etc.)": "mandatory_inclusions",
    "mandatory inclusions":                                         "mandatory_inclusions",
    "mandatory_inclusions":                                         "mandatory_inclusions",
    "required deliverables (select all that apply)":                "mandatory_inclusions",
    "projected content length/duration (estimate)":                 "mandatory_inclusions",
    "projected content length/duration":                            "mandatory_inclusions",
    "must include":                                                 "mandatory_inclusions",

    # reference_urls
    "reference urls (supporting documents, competitor examples, internal resources)": "reference_urls",
    "reference urls":                                               "reference_urls",
    "reference_urls":                                               "reference_urls",
    "references":                                                   "reference_urls",
    "urls":                                                         "reference_urls",
    "reference content":                                            "reference_urls",

    # free_text_notes
    "additional notes/context":                                     "free_text_notes",
    "additional notes":                                             "free_text_notes",
    "free text notes":                                              "free_text_notes",
    "free_text_notes":                                              "free_text_notes",
    "notes":                                                        "free_text_notes",
    "other notes":                                                  "free_text_notes",
    "anything else":                                                "free_text_notes",
}

# ---------------------------------------------------------------------------
# APPEND MAP  — supplementary columns merged into free_text_notes
APPEND_TO_NOTES: dict[str, str] = {
    "primary goal of the content (select up to 3)":    "Primary Goal",
    "desired tone and style":                          "Tone & Style",
    "projected content length/duration (estimate)":    "Est. Length",
    "urgency/priority level":                          "Urgency",
    "priority level":                                  "Urgency",
    "target deadline for draft submission":            "Deadline",
    "target deadline":                                 "Deadline",
    "date submitted":                                  "Submitted",
    "budget allocation (usd)":                         "Budget",
    "key contact email address":                       "Contact",
}

REQUIRED_FIELDS = [
    "brand_name", "content_type", "topic",
    "key_message", "target_audience",
    "mandatory_inclusions", "reference_urls", "free_text_notes"
]


def _get_service():
    creds = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_JSON, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def _get_first_sheet_name(service) -> str:
    meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
    return meta["sheets"][0]["properties"]["title"]


def _load_processed() -> set:
    if PROCESSED_LOG.exists():
        return set(json.loads(PROCESSED_LOG.read_text()))
    return set()


def _save_processed(processed: set):
    PROCESSED_LOG.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_LOG.write_text(json.dumps(list(processed)))


def _build_column_map(headers: list[str]) -> dict[int, str]:
    col_map = {}
    for i, h in enumerate(headers):
        key = h.strip().lower()
        if key in HEADER_MAP:
            field = HEADER_MAP[key]
            # Only take the first column that maps to a given field
            if field not in col_map.values():
                col_map[i] = field
    return col_map


def _build_append_map(headers: list[str]) -> dict[int, str]:
    """Returns {col_idx: label} for columns that should be appended to notes."""
    append_map = {}
    for i, h in enumerate(headers):
        key = h.strip().lower()
        if key in APPEND_TO_NOTES:
            append_map[i] = APPEND_TO_NOTES[key]
    return append_map


def fetch_new_briefs() -> list[RawBrief]:
    """
    Reads all rows from the Google Sheet using header-based column detection.
    Compatible with Google Forms (Timestamp auto-column) and manually-built sheets.
    Supplementary fields (urgency, deadline, budget) are appended to free_text_notes.
    """
    service    = _get_service()
    processed  = _load_processed()
    sheet_name = _get_first_sheet_name(service)

    result = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=f"{sheet_name}!A1:Z1000"
    ).execute()

    all_rows = result.get("values", [])
    if not all_rows:
        return []

    header_row  = all_rows[0]
    col_map     = _build_column_map(header_row)
    append_map  = _build_append_map(header_row)

    unmapped_required = [f for f in REQUIRED_FIELDS if f not in col_map.values()]
    if unmapped_required:
        print(f"[sheets] ⚠️  No column found for: {unmapped_required}")
        print(f"[sheets] Headers in sheet: {header_row}")

    data_rows  = all_rows[1:]
    new_briefs = []

    for i, row in enumerate(data_rows):
        row_id = f"row_{i + 2}"

        if row_id in processed:
            continue

        def cell(col_idx: int) -> str:
            return row[col_idx].strip() if col_idx < len(row) else ""

        def get_field(field: str) -> str:
            for idx, fname in col_map.items():
                if fname == field:
                    return cell(idx)
            return ""

        brand_name = get_field("brand_name")
        if not brand_name:
            continue  # skip blank rows

        # Build free_text_notes: base notes + appended supplementary fields
        base_notes = get_field("free_text_notes")
        appended_parts = []
        for col_idx, label in append_map.items():
            val = cell(col_idx)
            if val:
                appended_parts.append(f"{label}: {val}")

        combined_notes = base_notes
        if appended_parts:
            combined_notes = (base_notes + "\n" if base_notes else "") + " | ".join(appended_parts)

        brief = RawBrief(
            row_id=row_id,
            brand_name=brand_name,
            content_type=get_field("content_type"),
            topic=get_field("topic"),
            key_message=get_field("key_message"),
            target_audience=get_field("target_audience"),
            mandatory_inclusions=get_field("mandatory_inclusions"),
            reference_urls=get_field("reference_urls"),
            free_text_notes=combined_notes,
        )
        new_briefs.append(brief)
        processed.add(row_id)

    if new_briefs:
        _save_processed(processed)

    return new_briefs


def mark_row_processed(row_id: str):
    processed = _load_processed()
    processed.add(row_id)
    _save_processed(processed)